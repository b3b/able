package org.able;

import android.app.Activity;
import android.content.Intent;
import android.content.Context;
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

        public BLE(PythonBluetooth python) {
                mPython = python;
                mContext = (Context) PythonActivity.mActivity;
                mBluetoothGatt = null;

                final BluetoothManager bluetoothManager =
                        (BluetoothManager) mContext.getSystemService(Context.BLUETOOTH_SERVICE);
                mBluetoothAdapter = bluetoothManager.getAdapter();
        }

        public BluetoothGatt getGatt() {
                return mBluetoothGatt;
        }

        public void startScan(int EnableBtCode) {
                Log.d(TAG, "startScan");
                if (mBluetoothAdapter == null || !mBluetoothAdapter.isEnabled()) {
                        Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                        PythonActivity.mActivity.startActivityForResult(enableBtIntent, EnableBtCode);
                        return;
                }
                if (mBluetoothAdapter.startLeScan(mLeScanCallback)) {
                        mScanning = true;
                        mPython.on_scan_started(true);
                } else {
                        mPython.on_scan_started(false);
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
                        mBluetoothGatt = device.connectGatt(mContext, false, mGattCallback);
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
                                mPython.on_connection_state_change(status, newState);
                        }

                        @Override
                        public void onServicesDiscovered(BluetoothGatt gatt, int status) {
                                if (status == BluetoothGatt.GATT_SUCCESS) {
                                        Log.d(TAG, "onServicesDiscovered - success");
                                        mBluetoothGattServices = mBluetoothGatt.getServices();
                                } else {
                                        Log.d(TAG, "onServicesDiscovered status:" + status);
                                        mBluetoothGattServices = null;
                                }
                                mPython.on_services(status, mBluetoothGattServices);
                        }

                        @Override
                        public void onCharacteristicChanged(BluetoothGatt gatt,
                                                            BluetoothGattCharacteristic characteristic) {
                                mPython.on_characteristic_changed(characteristic);
                        }

                        public void onCharacteristicRead(BluetoothGatt gatt,
                                                         BluetoothGattCharacteristic characteristic,
                                                         int status) {
                                mPython.on_characteristic_read(characteristic, status);
                        }

                        public void onCharacteristicWrite(BluetoothGatt gatt,
                                                          BluetoothGattCharacteristic characteristic,
                                                          int status) {
                                mPython.on_characteristic_write(characteristic, status);
                        }

                        public void onDescriptorRead(BluetoothGatt gatt, 
                                                     BluetoothGattDescriptor descriptor, 
                                                     int status) {
                                mPython.on_descriptor_read(descriptor, status);
                        }

                        public void onDescriptorWrite(BluetoothGatt gatt, 
                                                      BluetoothGattDescriptor descriptor, 
                                                      int status) {
                                mPython.on_descriptor_write(descriptor, status);
                        }

                };

        public boolean writeCharacteristic(BluetoothGattCharacteristic characteristic, byte[] data) {
                if (characteristic.setValue(data)) {
                        return mBluetoothGatt.writeCharacteristic(characteristic);
                }
                return false;
        }

        public boolean writeCharacteristicNoResponse(BluetoothGattCharacteristic characteristic, byte[] data) {
                if (characteristic.setValue(data)) {
                        characteristic.setWriteType(BluetoothGattCharacteristic.WRITE_TYPE_NO_RESPONSE);
                        return mBluetoothGatt.writeCharacteristic(characteristic);
                }
                return false;
        }

        public boolean readCharacteristic(BluetoothGattCharacteristic characteristic) {
                return mBluetoothGatt.readCharacteristic(characteristic);
        }
}
