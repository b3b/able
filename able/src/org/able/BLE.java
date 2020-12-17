package org.able;

import android.app.Activity;
import android.content.Intent;
import android.content.Context;
import android.content.pm.PackageManager;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothProfile;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothGattService;
import android.os.Handler;
import android.util.Log;
import java.util.List;
import org.kivy.android.PythonActivity;
import org.able.PythonBluetooth;


public class BLE {
        private String TAG = "BLE-python";
        private PythonBluetooth mPython;
        private Context mContext;
        private BluetoothAdapter mBluetoothAdapter;
        private BluetoothGatt mBluetoothGatt;
        private List<BluetoothGattService> mBluetoothGattServices;
        private boolean mScanning;

        public void showError(final String msg) {
                Log.d(TAG, msg);
                PythonActivity.mActivity.toastError(TAG + " error. " + msg);
                mPython.on_error(msg);
        }

        public BLE(PythonBluetooth python) {
                mPython = python;
                mContext = (Context) PythonActivity.mActivity;
                mBluetoothGatt = null;

                if (!mContext.getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)) {
                        showError("Device do not support Bluetooth Low Energy.");
                        return;
                }

                final BluetoothManager bluetoothManager =
                        (BluetoothManager) mContext.getSystemService(Context.BLUETOOTH_SERVICE);
                mBluetoothAdapter = bluetoothManager.getAdapter();
        }

        public BluetoothAdapter getAdapter(int EnableBtCode) {
                if (mBluetoothAdapter == null) {
                        showError("Device do not support Bluetooth Low Energy.");
                        return null;
                }
                if (!mBluetoothAdapter.isEnabled()) {
                        Log.d(TAG, "BLE adapter is not enabled");
                        Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                        PythonActivity.mActivity.startActivityForResult(enableBtIntent, EnableBtCode);
                        return null;
                }
                return mBluetoothAdapter;
        }

        public BluetoothGatt getGatt() {
                return mBluetoothGatt;
        }

        public void startScan(int EnableBtCode) {
                Log.d(TAG, "startScan");
                BluetoothAdapter adapter = getAdapter(EnableBtCode);
                if (adapter != null) {
                    Log.d(TAG, "BLE adapter is ready for scan");
                    if (adapter.startLeScan(mLeScanCallback)) {
                            Log.d(TAG, "BLE scan started successfully");
                            mScanning = true;
                            mPython.on_scan_started(true);
                    } else {
                            Log.d(TAG, "BLE scan not started");
                            mPython.on_scan_started(false);
                    }
                }
        }

        public void stopScan() {
                if (mScanning == true) {
                        Log.d(TAG, "stopScan");
                        mScanning = false;
                        mBluetoothAdapter.stopLeScan(mLeScanCallback);
                        mPython.on_scan_completed();
                }
        }

        private BluetoothAdapter.LeScanCallback mLeScanCallback =
                new BluetoothAdapter.LeScanCallback() {
                        @Override
                        public void onLeScan(final BluetoothDevice device, final int rssi, final byte[] scanRecord) {
                                PythonActivity.mActivity.runOnUiThread(new Runnable() {
                                                @Override
                                                public void run() {
                                                        mPython.on_device(device, rssi, scanRecord);
                                                }
                                        });
                        }
                };

        public void connectGatt(BluetoothDevice device) {
                Log.d(TAG, "connectGatt");
                if (mBluetoothGatt == null) {
                        mBluetoothGatt = device.connectGatt(mContext, false, mGattCallback, BluetoothDevice.TRANSPORT_LE);
                }
        }

        public void closeGatt() {
                Log.d(TAG, "closeGatt");
                if (mBluetoothGatt != null) {
                        mBluetoothGatt.close();
                        mBluetoothGatt = null;
                }
        }

        private final BluetoothGattCallback mGattCallback =
                new BluetoothGattCallback() {
                        @Override
                        public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState) {
                                if (newState == BluetoothProfile.STATE_CONNECTED) {
                                        Log.d(TAG, "Connected to GATT server, status:" + status);
                                } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                                        Log.d(TAG, "Disconnected from GATT server, status:" + status);
                                }
                                if (mBluetoothGatt == null) {
                                        mBluetoothGatt = gatt;
                                }
                                mPython.on_connection_state_change(status, newState);
                        }

                        @Override
                        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
                                if (status == BluetoothGatt.GATT_SUCCESS) {
                                        Log.d(TAG, "onServicesDiscovered - success");
                                        mBluetoothGattServices = mBluetoothGatt.getServices();
                                } else {
                                        showError("onServicesDiscovered status:" + status);
                                        mBluetoothGattServices = null;
                                }
                                mPython.on_services(status, mBluetoothGattServices);
                        }

                        @Override
                        public void onCharacteristicChanged(BluetoothGatt gatt,
                                                            BluetoothGattCharacteristic characteristic) {
                                mPython.on_characteristic_changed(characteristic);
                        }

                        @Override
                        public void onCharacteristicRead(BluetoothGatt gatt,
                                                         BluetoothGattCharacteristic characteristic,
                                                         int status) {
                                mPython.on_characteristic_read(characteristic, status);
                        }

                        @Override
                        public void onCharacteristicWrite(BluetoothGatt gatt,
                                                          BluetoothGattCharacteristic characteristic,
                                                          int status) {
                                mPython.on_characteristic_write(characteristic, status);
                        }

                        @Override
                        public void onDescriptorRead(BluetoothGatt gatt, 
                                                     BluetoothGattDescriptor descriptor, 
                                                     int status) {
                                mPython.on_descriptor_read(descriptor, status);
                        }

                        @Override
                        public void onDescriptorWrite(BluetoothGatt gatt, 
                                                      BluetoothGattDescriptor descriptor, 
                                                      int status) {
                                mPython.on_descriptor_write(descriptor, status);
                        }

                        @Override
			public void onReadRemoteRssi(BluetoothGatt gatt,
						     int rssi, int status) {
				mPython.on_rssi_updated(rssi, status);
			}

                        @Override
                        public void onMtuChanged(BluetoothGatt gatt,
                                                 int mtu, int status) {
                                Log.d(TAG, String.format("onMtuChanged mtu=%d status=%d", mtu, status));
				mPython.on_mtu_changed(mtu, status);
			}
                };

        public boolean writeCharacteristic(BluetoothGattCharacteristic characteristic, byte[] data, int writeType) {
                if (characteristic.setValue(data)) {
                        if (writeType != 0) {
                                characteristic.setWriteType(writeType);
                        }
                        return mBluetoothGatt.writeCharacteristic(characteristic);
                }
                return false;
        }

        public boolean readCharacteristic(BluetoothGattCharacteristic characteristic) {
                return mBluetoothGatt.readCharacteristic(characteristic);
        }

	public boolean readRemoteRssi() {
		return mBluetoothGatt.readRemoteRssi();
	}
}
