---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Setup

```python
%run init.ipynb
```

```python
%%there
class BLE(BluetoothDispatcher):

    def on_scan_started(self, success):
        results.started = success
        
    def on_scan_completed(self):
        results.completed = 1
        
    def on_device(self, device, rssi, advertisement):
        results.devices.append(device)

ble = BLE()
```

# Test device is found with filter by name

```python
%%there
results =  Results()

filters = ArrayList()
filters.add(
    ScanFilterBuilder().setDeviceName("KivyBLETest").build()
)

ble.start_scan(filters=filters)
```

```python
sleep(10)
```

```python
%%there
ble.stop_scan()
```

```python
sleep(2)
```

```python
%%there
print(set([dev.getName() for dev in results.devices]))
```

# Test device is not found: filtered out by name

```python
%%there
results =  Results()

filters = ArrayList()
filters.add(
    ScanFilterBuilder().setDeviceName("No-such-device-8458e2e35158").build()
)

ble.start_scan(filters=filters)
```

```python
sleep(10)
```

```python
%%there
ble.stop_scan()
```

```python
sleep(2)
```

```python
%%there
ble.stop_scan()

print(results.devices)
```
