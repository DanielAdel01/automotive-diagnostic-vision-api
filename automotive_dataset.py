
data = [
    {
        "prompt": "Diagnostic Trouble Code P0301 means",
        "completion": " a misfire has been detected in cylinder 1."
    },
    {
        "prompt": "Diagnostic Trouble Code P0420 means",
        "completion": " catalyst system efficiency is below the required threshold on bank 1."
    },
    {
        "prompt": "Diagnostic Trouble Code P0171 means",
        "completion": " the fuel system is running too lean on bank 1."
    },
    {
        "prompt": "Diagnostic Trouble Code P0300 means",
        "completion": " random or multiple cylinder misfires have been detected."
    },
    {
        "prompt": "Diagnostic Trouble Code P0128 means",
        "completion": " the engine coolant temperature is below the thermostat regulating temperature expected by the control system."
    },
    {
        "prompt": "Diagnostic Trouble Code P0302 means",
        "completion": " a misfire has been detected in cylinder 2."
    },
    {
        "prompt": "Diagnostic Trouble Code P0303 means",
        "completion": " a misfire has been detected in cylinder 3."
    },
    {
        "prompt": "Diagnostic Trouble Code P0304 means",
        "completion": " a misfire has been detected in cylinder 4."
    },
    {
        "prompt": "Diagnostic Trouble Code P0172 means",
        "completion": " the fuel system is running too rich on bank 1."
    },
    {
        "prompt": "Diagnostic Trouble Code P0174 means",
        "completion": " the fuel system is running too lean on bank 2."
    },
    {
        "prompt": "Diagnostic Trouble Code P0175 means",
        "completion": " the fuel system is running too rich on bank 2."
    },
    {
        "prompt": "Diagnostic Trouble Code P0130 means",
        "completion": " a fault has been detected in the bank 1 sensor 1 oxygen sensor circuit."
    },
    {
        "prompt": "Diagnostic Trouble Code P0133 means",
        "completion": " the bank 1 sensor 1 oxygen sensor response is too slow."
    },
    {
        "prompt": "Diagnostic Trouble Code P0135 means",
        "completion": " a fault has been detected in the bank 1 sensor 1 oxygen sensor heater circuit."
    },
    {
        "prompt": "Diagnostic Trouble Code P0141 means",
        "completion": " a fault has been detected in the bank 1 sensor 2 oxygen sensor heater circuit."
    },
    {
        "prompt": "Diagnostic Trouble Code P0401 means",
        "completion": " exhaust gas recirculation flow is insufficient."
    },
    {
        "prompt": "Diagnostic Trouble Code P0402 means",
        "completion": " excessive exhaust gas recirculation flow has been detected."
    },
    {
        "prompt": "Diagnostic Trouble Code P0442 means",
        "completion": " a small leak has been detected in the evaporative emissions system."
    },
    {
        "prompt": "Diagnostic Trouble Code P0455 means",
        "completion": " a large leak or a major leak condition has been detected in the evaporative emissions system."
    },
    {
        "prompt": "Diagnostic Trouble Code P0456 means",
        "completion": " a very small leak has been detected in the evaporative emissions system."
    },
    {
        "prompt": "Diagnostic Trouble Code P0500 means",
        "completion": " a fault has been detected in the vehicle speed sensor signal."
    },
    {
        "prompt": "Diagnostic Trouble Code P0700 means",
        "completion": " the transmission control system has requested the engine control module to illuminate the malfunction indicator lamp."
    },
    {
        "prompt": "Diagnostic Trouble Code P0715 means",
        "completion": " a fault has been detected in the transmission input or turbine speed sensor circuit."
    },
    {
        "prompt": "Diagnostic Trouble Code P0730 means",
        "completion": " the transmission control system has detected an incorrect gear ratio."
    },
    {
        "prompt": "Diagnostic Trouble Code P0115 means",
        "completion": " a fault has been detected in the engine coolant temperature sensor circuit."
    },
    {
        "prompt": "Diagnostic Trouble Code P0118 means",
        "completion": " the engine coolant temperature sensor circuit input is too high."
    },
    {
        "prompt": "Diagnostic Trouble Code P0101 means",
        "completion": " the mass or volume air flow sensor signal is outside the expected range or performance."
    },
    {
        "prompt": "Diagnostic Trouble Code P0102 means",
        "completion": " the mass or volume air flow sensor circuit input is too low."
    },
    {
        "prompt": "Diagnostic Trouble Code P0103 means",
        "completion": " the mass or volume air flow sensor circuit input is too high."
    },
    {
        "prompt": "Diagnostic Trouble Code P0325 means",
        "completion": " a fault has been detected in the knock sensor 1 circuit on bank 1."
    },
]


if __name__ == "__main__":
    print("Number of DTC examples:", len(data))
    for item in data[:5]:
        print(item["prompt"] + item["completion"])

