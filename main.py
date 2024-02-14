import adbutils
from lxml import etree
import time


def get_input_fields():
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    devices = adb.device_list()

    if not devices:
        raise Exception("No devices connected")

    device = devices[0]  # Use the first connected device
    device_name = device.shell("getprop ro.product.model").strip()
    print(f"Device connected: {device.serial} ({device_name})")

    print("Dumping UI hierarchy...")
    start_time = time.time()
    xml_dump = device.shell("uiautomator dump /dev/tty && cat /dev/tty")
    end_time = time.time()
    print("UI hierarchy dumped in {:.2f} seconds.".format(end_time - start_time))

    print("Parsing XML...")
    root = etree.fromstring(xml_dump.encode("utf-8"))

    print("Extracting input fields...")
    input_fields = root.xpath(".//node[@class='android.widget.EditText']")

    fields_info = []
    for i, field in enumerate(input_fields, start=1):
        field_info = {
            "text": field.attrib.get("text", ""),
            "resource_id": field.attrib.get("resource-id", ""),
            "bounds": field.attrib.get("bounds", ""),
        }
        fields_info.append(field_info)
        # Simple progress bar
        progress = int((i / len(input_fields)) * 100)
        print(f"Progress: {progress}%", end="\r")

    print("\nExtraction complete.")
    return fields_info


# Example usage
input_fields = get_input_fields()
print(input_fields)
