const int pin = 3;  // Utilisez le pin correct selon votre schéma électrique

void setup() {
  pinMode(pin, OUTPUT);  // Définir le pin comme sortie
}

void loop() {
  digitalWrite(pin, HIGH);  // Activer l'électroaimant
  Serial.print("on");
  delay(3000);              // Attendre 10 secondes
  digitalWrite(pin, LOW);   // Désactiver l'électroaimant
  Serial.print("off");
  delay(3000);              // Attendre 10 secondes
}
