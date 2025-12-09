// Step 3 
bool startLoop = false;
bool restart = false;
unsigned long startTime = 0;
unsigned long elapsedTime = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(1000000, SERIAL_8N1);
  
  while(!startLoop) {
    if(Serial.available()) {
      startLoop = ((char)(Serial.read()) == 'r');
    }
  }
  
  // Démarrage du comptage temps à l'entrée dans la boucle
  startTime = millis();
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  
  // Calcul du temps écoulé en secondes
  elapsedTime = (millis() - startTime) / 1000;
  
  // Affichage du comptage temporel
  Serial.println(elapsedTime);
  
  // Gestion du redémarrage
  if(Serial.available()) {
    restart = ((char)(Serial.read()) == 's');
    if(restart) {
      __NVIC_SystemReset();
    }
  }
  
  delay(100); // Petit délai pour vérifier (à supprimer au step 4)
}
