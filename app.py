import adbutils
from lxml import etree
import time
import sys


def launch_app(device, package_name):
    print(f"Launching application: {package_name}")
    device.shell(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")


def get_input_fields(device):
    print("Dumping UI hierarchy...")
    start_time = time.time()
    xml_dump = device.shell("uiautomator dump /dev/tty && cat /dev/tty")
    end_time = time.time()
    print(f"UI hierarchy dumped in {end_time - start_time:.2f} seconds.")

    print("Parsing XML...")
    root = etree.fromstring(xml_dump.encode("utf-8"))

    print("Extracting input fields...")
    input_fields = root.xpath(".//node[@class='android.widget.EditText']")

    fields_info = []
    for field in input_fields:
        field_info = {
            "text": field.attrib.get("text", ""),
            "resource_id": field.attrib.get("resource-id", ""),
            "bounds": field.attrib.get("bounds", ""),
        }
        fields_info.append(field_info)

    print("Extraction complete.")
    return fields_info


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <package_name>")
        sys.exit(1)

    package_name = sys.argv[1]

    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    devices = adb.device_list()

    if not devices:
        raise Exception("No devices connected")

    device = devices[0]
    device_name = device.shell("getprop ro.product.model").strip()
    print(f"Device connected: {device.serial} ({device_name})")

    launch_app(device, package_name)

    time.sleep(5)

    input_fields = get_input_fields(device)
    print(input_fields)


if __name__ == "__main__":
    main()
