class HealthDataAnalyzer:

    def __init__(self, Systolic_Pressure=None, Diastolic_Pressure=None, Hours=None, BPM=None, Breaths_Per_Minute=None):
        self.Systolic_Pressure = Systolic_Pressure
        self.Diastolic_Pressure = Diastolic_Pressure
        self.Hours = Hours
        self.BPM = BPM
        self.Breaths_Per_Minute = Breaths_Per_Minute

    def Blood_Pressure(self):
        if self.Systolic_Pressure <= 90 and self.Diastolic_Pressure <= 60:
            Blood_Pressure_Category = "Blood Pressure: Category E - Low Blood Pressure"
            return Blood_Pressure_Category
        elif (91 <= self.Systolic_Pressure <= 120) and (61 <= self.Diastolic_Pressure <= 80):
            Blood_Pressure_Category = "Blood Pressure: Category D - Normal Blood Pressure"
            return Blood_Pressure_Category
        elif (121 <= self.Systolic_Pressure <= 129) and (80 <= self.Diastolic_Pressure <= 84):
            Blood_Pressure_Category = "Blood Pressure: Category C - Slightly Elevated Blood Pressure"
            return Blood_Pressure_Category
        elif (130 <= self.Systolic_Pressure <= 139) and (85 <= self.Diastolic_Pressure <= 89):
            Blood_Pressure_Category = "Blood Pressure: Category B - Moderately Elevated Blood Pressure"
            return Blood_Pressure_Category
        elif self.Systolic_Pressure >= 140 and self.Diastolic_Pressure >= 90:
            Blood_Pressure_Category = "Blood Pressure: Category A - High Blood Pressure"
            return Blood_Pressure_Category
        else:
            raise Exception

    def Sleeping_hours(self):
        if 8.00 <= self.Hours <= 8.59:
            Hours_Category = "Sleeping Hours: Category E - Very Good Quality Of Sleep"
            return Hours_Category
        elif 7.00 <= self.Hours <= 7.59 or 9.00 <= self.Hours <= 9.59:
            Hours_Category = "Sleeping Hours: Category D - Good Quality Of Sleep"
            return Hours_Category
        elif 6.00 <= self.Hours <= 6.59 or 10.00 <= self.Hours <= 10.59:
            Hours_Category = "Sleeping Hours: Category C - Average Quality Of Sleep"
            return Hours_Category
        elif 5.00 <= self.Hours <= 5.59 or 11.00 <= self.Hours <= 11.59:
            Hours_Category = "Sleeping Hours: Category B - Poor Quality Of Sleep"
            return Hours_Category
        elif self.Hours < 5.00 or self.Hours > 12.00:
            Hours_Category = "Sleeping Hours: Category A - Very Poor Quality Of Sleep"
            return Hours_Category
        else:
            raise Exception

    def Heart_Rate(self):
        if self.BPM <= 59:
            BPM_Category = "Heart Rate: Category E - Low Heart Beat"
            return BPM_Category
        elif 60 <= self.BPM <= 100:
            BPM_Category = "Heart Rate: Category D - Normal Heart Beat"
            return BPM_Category
        elif 101 <= self.BPM <= 110:
            BPM_Category = "Heart Rate: Category C - Slightly Elevated Heart Beat"
            return BPM_Category
        elif 111 <= self.BPM <= 120:
            BPM_Category = "Heart Rate: Category B - Moderately Elevated Heart Beat"
            return BPM_Category
        elif self.BPM >= 121:
            BPM_Category = "Heart Rate: Category A - High Heart Beat"
            return BPM_Category
        else:
            raise Exception

    def Breathing_Speed(self):
        if self.Breaths_Per_Minute <= 11:
            Breaths_Per_Minute_Category = "Breaths Per Minute: Category E - Low Breathing Speed"
            return Breaths_Per_Minute_Category
        elif 12 <= self.Breaths_Per_Minute <= 20:
            Breaths_Per_Minute_Category = "Breaths Per Minute: Category D - Normal Breathing Speed"
            return Breaths_Per_Minute_Category
        elif 21 <= self.Breaths_Per_Minute <= 24:
            Breaths_Per_Minute_Category = "Breaths Per Minute: Category C - Slightly Elevated Breathing Speed"
            return Breaths_Per_Minute_Category
        elif 25 <= self.Breaths_Per_Minute <= 29:
            Breaths_Per_Minute_Category = "Breaths Per Minute: Category B - Moderately Elevated Breathing Speed"
            return Breaths_Per_Minute_Category
        elif self.Breaths_Per_Minute >= 30:
            Breaths_Per_Minute_Category = "Breaths Per Minute: Category A - High Breathing Speed"
            return Breaths_Per_Minute_Category
        else:
            raise Exception


while True:
    try:
        Name = str(input("Enter your name: ")).strip()
        if Name.replace(" ","").isalpha():
            break
        else:
            print("Please enter your name in alphabetical characters only.\n")
    except:
        print("Please enter your name in alphabetical characters only.\n")

while True:
    try:
        Systolic_Pressure_Input, Diastolic_Pressure_Input = input("\nInput your blood pressure in (Systolic/Diastolic) mmHg: ").strip().split("/")
        HealthDataAnalyzer(Systolic_Pressure=int(Systolic_Pressure_Input), Diastolic_Pressure=int(Diastolic_Pressure_Input)).Blood_Pressure()
        break
    except:
        print("Invalid Blood Pressure values. Please make sure Systolic and Diastolic pressures are within the valid range.")

while True:
    try:
        Hours_Input = input("Input your sleeping hours in (HH.MM): ").strip()
        HealthDataAnalyzer(Hours=float(Hours_Input)).Sleeping_hours()
        break
    except:
        print("Please enter a valid numeric value for hours slept.")

while True:
    try:
        BPM_Input = input("Input your heart beats per minute: ").strip()
        HealthDataAnalyzer(BPM=int(BPM_Input)).Heart_Rate()
        break
    except:
        print("Please enter a valid numeric value for heart rate.")

while True:
    try:
        Breaths_Per_Minute_Input = input("Input your breaths per minute: ").strip()
        HealthDataAnalyzer(Breaths_Per_Minute=int(Breaths_Per_Minute_Input)).Breathing_Speed()
        break
    except:
        print("Please enter a valid numeric value for breaths per minute.")

print(f"\nHello! {Name},")
print(HealthDataAnalyzer(Systolic_Pressure=int(Systolic_Pressure_Input), Diastolic_Pressure=int(Diastolic_Pressure_Input)).Blood_Pressure())
print(HealthDataAnalyzer(Hours=float(Hours_Input)).Sleeping_hours())
print(HealthDataAnalyzer(BPM=int(BPM_Input)).Heart_Rate())
print(HealthDataAnalyzer(Breaths_Per_Minute=int(Breaths_Per_Minute_Input)).Breathing_Speed())
