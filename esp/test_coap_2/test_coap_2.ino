#include <WiFi.h>
#include <coap-simple.h>
#include <ArduinoJson.h>

WiFiUDP udp;
Coap coap(udp, 256);

IPAddress SERVER_IP(192,168,1,13);
const int SERVER_PORT = 5683;

// === CONFIG ===
const unsigned long SEND_PERIOD_MS = 5000;   // interval kirim sensor
const unsigned long METRIC_DEFER_MS = 50;    // tunda kirim metric setelah ACK

// === STATE ===
struct Pending {
  uint32_t send_ms;
  size_t   bytes;
  uint16_t seq;
  bool     valid;
} pending_last = {0,0,0,false};

struct MetricBuf {
  char   buf[256];
  size_t len;
  bool   queued;
  uint32_t queued_at_ms;
} metric = {{0},0,false,0};

uint16_t seq = 0;
bool req_in_flight = false;
unsigned long last_send_ms = 0;

void on_response(CoapPacket &pkt, IPAddress ip, int port) {
  const uint32_t resp_ms = millis();

  // Parse seq yang di-echo server (opsional)
  StaticJsonDocument<256> doc;
  uint16_t rseq = 0;
  if (deserializeJson(doc, (const char*)pkt.payload, pkt.payloadlen) == DeserializationError::Ok) {
    rseq = doc["seq"] | 0;
  }
  // Fallback kalau server tidak echo seq
  if (rseq == 0 && pending_last.valid) rseq = pending_last.seq;

  // Hitung RTT dari pending_last
  uint32_t rtt = 0;
  if (pending_last.valid && rseq == pending_last.seq) {
    rtt = resp_ms - pending_last.send_ms;
  }

  // Queue metrics (DEFERRED, jangan TX di callback)
  StaticJsonDocument<256> m;
  m["seq"]            = rseq;
  m["client_send_ms"] = pending_last.send_ms;
  m["client_resp_ms"] = resp_ms;
  m["rtt_ms"]         = rtt;
  m["payload_bytes"]  = pending_last.bytes;

  metric.len = serializeJson(m, metric.buf, sizeof(metric.buf));
  metric.queued = true;
  metric.queued_at_ms = resp_ms;

  // Request selesai
  req_in_flight = false;
  pending_last.valid = false;

  Serial.printf("[ACK] seq=%u rtt=%lums bytes=%u (queued metric %uB)\n",
                rseq, (unsigned long)rtt, (unsigned)pending_last.bytes, (unsigned)metric.len);
}

void setup() {
  Serial.begin(115200);
  WiFi.begin("duFIFA","Fahri8013");
  while (WiFi.status()!=WL_CONNECTED) { delay(250); Serial.print("."); }
  Serial.println("\nWiFi OK");

  coap.start();
  coap.response(on_response);
}

void loop() {
  // Proses RX/timeouts CoAP (single-threaded)
  coap.loop();

  const uint32_t now = millis();

  // 1) Kirim METRIC yang di-defer (di luar callback) setelah jeda kecil
  if (metric.queued && !req_in_flight && (now - metric.queued_at_ms >= METRIC_DEFER_MS)) {
    // Fire-and-forget; kalau mau tunggu ACK bisa set flag sendiri
    coap.put(SERVER_IP, SERVER_PORT, "metrics", metric.buf, metric.len);
    metric.queued = false;
    Serial.println("[METRIC] → /metrics posted");
  }

  // 2) Kirim data sensor periodik (1 in-flight at a time)
  if (!req_in_flight && (now - last_send_ms >= SEND_PERIOD_MS)) {
    // Dummy sensor
    float tA=28.5, tB=27.5, hA=65, hB=70;

    StaticJsonDocument<256> j;
    j["seq"] = seq;
    j["client_send_ms"] = now;
    j["temperatureAtas"]  = tA;
    j["temperatureBawah"] = tB;
    j["humidityAtas"]     = hA;
    j["humidityBawah"]    = hB;

    String payload;
    serializeJson(j, payload);

    pending_last.send_ms = now;
    pending_last.bytes   = payload.length();
    pending_last.seq     = seq;
    pending_last.valid   = true;

    coap.put(SERVER_IP, SERVER_PORT, "environment", payload.c_str(), payload.length());

    req_in_flight = true;
    last_send_ms = now;
    Serial.printf("[PUT]  → /environment seq=%u len=%u\n", seq, (unsigned)payload.length());
    seq++;
  }

  // 3) Yield CPU ke WiFi/UDP & hindari pegging 100% (fix “Hello World” spam)
  delay(10); // atau vTaskDelay(1), yield(), dll.
}
