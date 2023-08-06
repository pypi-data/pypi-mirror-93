inm_user_settings_descriptor = {
    "about": {
        "title": "V2.5 configuration",
        "description": """This is the configuration for the ADM v2.5. 
        0. Set the VPE basic control to "Indoor Heading";
        1. Turn on the HSIE;
        2. Reset the INM;
        3. No data strings outputs; 
        4. All neccesary binary data outputs; 
        5. Window size of accelerometer filter is 100 of 800 Hz, it means that the FIR low-pass filter cutoff frequency is 8 Hz."""
    },
    "content": {
        "0": {
            "function": "SYSTEM_SET_ASYNC_DATA_OUTPUT_TYPE",
            "args": {
                "ADOR": "N/A",
                "SerialPort": "CURRENT"
            }
        },
        "1": {
            "function": "SYSTEM_RESET",
            "args": {}
        },
        "2": {
            "function": "ATTITUDE_SET_VPE_BASIC_CONTROL",
            "args": {
                "Enable": "ENABLE",
                "HeadingMode": "INDOOR",
                "FilteringMode": "MODE_1",
                "TuningMode": "MODE_1"
            }
        },
        "3": {
            "function": "HSIE_SET_MAGNETOMETER_CALIBRATION_CONTROL",
            "args": {
                "HSIMode": "RUN",
                "HSIOutput": "USE",
                "ConvergeRate": 4
            }
        },
        "4": {
            "function": "SYSTEM_SET_BINARY_OUTPUT_REGISTERS",
            "args": {
                "Binary_output_register_number": 1,
                "AsyncMode": "SERIAL_PORT_1",
                "RateDivisor": 80,
                "OutputGroup_fields": {
                    "GROUP_1": [
                        "MagPres",
                        "YawPitchRoll",
                        "Accel",
                        "AngularRate"
                    ]
                }
            }
        },
        "5": {
            "function": "IMU_SET_FILTERING_CONFIGURATION",
            "args": {
                "MagWindowSize": 0,
                "AccelWindowSize": 100,
                "GyroWindowSize": 4,
                "TempWindowSize": 4,
                "PresWindowSize": 0,
                "MagFilterMode": "NULL",
                "AccelFilterMode": "BOTH",
                "GyroFilterMode": "BOTH",
                "TempFilterMode": "BOTH",
                "PresFilterMode": "NULL"
            }
        }
    }
}
