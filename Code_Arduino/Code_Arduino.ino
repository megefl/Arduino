// Step 5 - Sonar HC-SR04 avec NewPing + Step 4
#include <NewPing.h>

#define TRIG_PIN 9
#define ECHO_PIN 10
#define MAX_DISTANCE 400  // cm max

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);  // ← Librairie !

bool startLoop = false;
bool restart = false;
bool firstLoop = true;
unsigned long initTime, time;
char serialMessage[64];

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(1000000, SERIAL_8N1);
  
  while(!startLoop) {
    if(Serial.available()) {
      startLoop = ((char)(Serial.read()) == 'r');
    }
  }
}

void loop() {  
  if(firstLoop) {
    digitalWrite(LED_BUILTIN, HIGH);
    firstLoop = false;
    initTime = micros();
    time = 0;
  } else {
    time = micros() - initTime;
  }
  
  // ← SONAR : Mesure distance en cm
  unsigned int distance_cm = sonar.ping_cm();  // ← NewPing !
  
  // ← Format "temps:distance_cm" avec sprintf (comme demandé)
  sprintf(serialMessage, "%lu:%d", time, distance_cm);
  
  Serial.println(serialMessage);
  Serial.flush();
  
  // Redémarrage
  if(Serial.available()) {
    restart = ((char)(Serial.read()) == 's');
    if(restart) __NVIC_SystemReset();
  }
}
