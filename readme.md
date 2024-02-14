# ADB Input Field Extractor

This Python script uses the Android Debug Bridge (ADB) to extract information about input fields from the currently displayed screen of a connected Android device.

## Requirements

- Python 3.x
- [adbutils](https://pypi.org/project/adbutils/)
- [lxml](https://pypi.org/project/lxml/)
- ADB (Android Debug Bridge) installed and added to the system's PATH

## Setup

1. **Install Python Dependencies:**

   ```bash
   pip install -r requirments.txt
   ```

   **Enable USB Debugging on your Android device:**

1. Go to `Settings` > `About phone` > Tap `Build number` `7 times` to enable Developer
   options.
1. Go back to `Settings` > `System` > `Developer options` > `Enable USB debugging`.
   Connect your Android device to your computer via USB.

## Usage

Run the Script:

```
python main.py
```

The script will connect to the first available device, dump the UI hierarchy, parse the XML, and extract information about input fields such as text, resource ID, and bounds.

Output:
The extracted input field information will be printed to the console in the following format:

```
[
   {
       'text': 'example text',
       'resource_id': 'com.example:id/inputField',
       'bounds': '[0,0][100,100]'
   },
   ...
]
```

## Notes

The script currently only extracts information from input fields of type
android.widget.EditText.
Ensure that the screen you want to analyze is displayed on the device before running the
script.
The extraction process might take a few seconds, depending on the complexity of the UI.
