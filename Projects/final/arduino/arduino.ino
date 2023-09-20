// Economic Class LEDs
#define EC 1    // Economic Class ID
#define ECG 13  // Economic Class Green LED
#define ECY 12  // Economic Class Yellow LED
#define ECR 11  // Economic Class Red LED

// Business Class LEDs
#define BC 2    // Business Class ID
#define BCG 10  // Business Class Green LED
#define BCY 9   // Business Class Yellow LED
#define BCR 8   // Business Class Red LED

// Pilot Cabin LEDs
#define PC 3    // Pilot Cabin ID
#define PCG 7   // Pilot Cabin Green LED
#define PCY 6   // Pilot Cabin Yellow LED
#define PCR 5   // Pilot Cabin Red LED

// Motor
#define MUP 3   // Motor Upper Pin
#define MLP 4   // Motor Lower Pin

// Buzzer
#define BUZ 2   // Buzzzer Pin

void setup() {
  // Register all LEDs (Default state: LOW)
  pinMode(ECG, OUTPUT); digitalWrite(ECG, LOW);
  pinMode(ECY, OUTPUT); digitalWrite(ECY, LOW);
  pinMode(ECR, OUTPUT); digitalWrite(ECR, LOW);
  pinMode(BCG, OUTPUT); digitalWrite(BCG, LOW);
  pinMode(BCY, OUTPUT); digitalWrite(BCY, LOW);
  pinMode(BCR, OUTPUT); digitalWrite(BCR, LOW);
  pinMode(PCG, OUTPUT); digitalWrite(PCG, LOW);
  pinMode(PCY, OUTPUT); digitalWrite(PCY, LOW);
  pinMode(PCR, OUTPUT); digitalWrite(PCR, LOW);
  // Register Motor and disable
  pinMode(MUP, OUTPUT); digitalWrite(MUP, LOW);
  pinMode(MLP, OUTPUT); digitalWrite(MLP, LOW);
  // Register Buzzer and disable
  pinMode(BUZ, OUTPUT); digitalWrite(BUZ, LOW);

  // All pressure levels normal in the beginning
  safePressure(1);
  safePressure(2);
  safePressure(3);
}

void loop() {
  for (int i = 1; i <= 3; i++) {
    delay(200);
    unSafePressure(i);
    delay(100);
    increasePressure(i);
    delay(200);
    safePressure(i); 
  }
}

void safePressure(int cabin) {
  /* Turns off Buzzer & Turns on Cabin's Green LED */
  switch (cabin) {
    case EC:
      digitalWrite(ECG, HIGH);
      digitalWrite(ECY, LOW);
      digitalWrite(ECR, LOW);
      disableBuzzer();
      stopMotor();
      break;
    case BC:
      digitalWrite(BCG, HIGH);
      digitalWrite(BCY, LOW);
      digitalWrite(BCR, LOW);
      disableBuzzer();
      stopMotor();
      break;
    case PC:
      digitalWrite(PCG, HIGH);
      digitalWrite(PCY, LOW);
      digitalWrite(PCR, LOW);
      disableBuzzer();
      stopMotor();
      break;
  }
}

void unSafePressure(int cabin) {
  /* Turns on Buzzer & Turns on Cabin's Red LED */
  switch (cabin) {
    case EC:
      digitalWrite(ECG, LOW);
      digitalWrite(ECY, LOW);
      digitalWrite(ECR, HIGH);
      enableBuzzer();
      break;
    case BC:
      digitalWrite(BCG, LOW);
      digitalWrite(BCY, LOW);
      digitalWrite(BCR, HIGH);
      enableBuzzer();
      break;
    case PC:
      digitalWrite(PCG, LOW);
      digitalWrite(PCY, LOW);
      digitalWrite(PCR, HIGH);
      enableBuzzer();
      break;
  }
}

void increasePressure(int cabin) {
  /* Motor Clockwise Rotation */
  switch (cabin) {
    case EC:
      digitalWrite(ECG, LOW);
      digitalWrite(ECY, HIGH);
      digitalWrite(ECR, LOW);
      turnMotorClockwise();
      break;
    case BC:
      digitalWrite(BCG, LOW);
      digitalWrite(BCY, HIGH);
      digitalWrite(BCR, LOW);
      turnMotorClockwise();
      break;
    case PC:
      digitalWrite(PCG, LOW);
      digitalWrite(PCY, HIGH);
      digitalWrite(PCR, LOW);
      turnMotorClockwise();
      break;
  }
}

void decreasePressure(int cabin) {
  /* Motor Counter Clockwise Rotation */
  switch (cabin) {
    case EC:
      digitalWrite(ECG, LOW);
      digitalWrite(ECY, HIGH);
      digitalWrite(ECR, LOW);
      turnMotorCounterClockwise();
      break;
    case BC:
      digitalWrite(BCG, LOW);
      digitalWrite(BCY, HIGH);
      digitalWrite(BCR, LOW);
      turnMotorCounterClockwise();
      break;
    case PC:
      digitalWrite(PCG, LOW);
      digitalWrite(PCY, HIGH);
      digitalWrite(PCR, LOW);
      turnMotorCounterClockwise();
      break;
  }
}

void stopMotor() {
  /* Set both Motor pins either HIGH or LOW */
  digitalWrite(MUP, HIGH);
  digitalWrite(MLP, HIGH);
}

void turnMotorClockwise() {
  /* Set both Motor pins either HIGH or LOW */
  digitalWrite(MUP, HIGH);
  digitalWrite(MLP, LOW);
}

void turnMotorCounterClockwise() {
  /* Set both Motor pins either HIGH or LOW */
  digitalWrite(MUP, LOW);
  digitalWrite(MLP, HIGH);
}

void enableBuzzer() {
  /* Enables Buzzer to Beeeep */
  digitalWrite(BUZ, HIGH);
}

void disableBuzzer() {
  /* Disables Buzzer not to Beeeep */
  digitalWrite(BUZ, LOW);
}
