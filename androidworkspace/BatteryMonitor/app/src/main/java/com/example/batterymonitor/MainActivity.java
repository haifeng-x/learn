package com.example.batterymonitor;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.BatteryManager;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.lang.reflect.Method;
import java.io.FileReader;


public class MainActivity extends AppCompatActivity {

    private TextView batterLevel;
    private BroadcastReceiver batteryLevelRcvr;
    private IntentFilter batteryLevelFilter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button1 = (Button) findViewById(R.id.button_1);
        button1.setOnClickListener(new View.OnClickListener(){
            @Override
            public  void onClick(View v){
                Toast.makeText(MainActivity.this,getCurrent(),
                        Toast.LENGTH_SHORT).show();
            }
        });
        batterLevel = (TextView)findViewById(R.id.batteryLevel);
        monitorBatteryState();
    }

    private String getCurrent() {
        String result = "null";
        try {
            Thread.sleep(5000);
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            Class systemProperties = Class.forName("android.os.SystemProperties");
            Method get = systemProperties.getDeclaredMethod("get", String.class);
            String filePath ="/sys/class/power_supply/battery/current_now";

                int current = Math.round(getMeanCurrentVal(filePath, 50, 1) / 1000.0f);
                //int current = readFile("/sys/class/power_supply/battery/current_now", 0) / 10;
                int voltage = readFile("/sys/class/power_supply/battery/voltage_now", 0) / 1000;
                // 高通平台该值小于0时电池处于放电状态，大于0时处于充电状态
                if (current < 0) {
                    result = "充电电流为：" + (-current) + "mA, 电压为：" + voltage + "mV";
                } else {
                    result = "放电电流为：" + current + "mA, 电压为：" + voltage + "mV";
                }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return result;
    }

    /**
     * 获取平均电流值
     * 获取 filePath 文件 totalCount 次数的平均值，每次采样间隔 intervalMs 时间
     */
    private float getMeanCurrentVal(String filePath, int totalCount, int intervalMs) {
        float meanVal = 0.0f;
        if (totalCount <= 0) {
            return 0.0f;
        }
        for (int i = 0; i < totalCount; i++) {
            try {
                float f = Float.valueOf(readFile(filePath, 0));
                meanVal += f / totalCount;
            } catch (Exception e) {
                e.printStackTrace();
            }
            if (intervalMs <= 0) {
                continue;
            }
            try {
                Thread.sleep(intervalMs);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        return meanVal;
    }

    private int readFile(String path, int defaultValue) {
        try {
            BufferedReader bufferedReader = new BufferedReader(new FileReader(                    path));
            int i = Integer.parseInt(bufferedReader.readLine(), 10);
            bufferedReader.close();
            return i;
        } catch (Exception localException) {
        }
        return defaultValue;
    }

    private void monitorBatteryState(){
        batteryLevelRcvr = new BroadcastReceiver(){

            @Override
            public void onReceive(Context context, Intent intent) {
                // TODO Auto-generated method stub
                StringBuilder sb = new StringBuilder();
                int rawlevel = intent.getIntExtra("level", -1);
                int scale = intent.getIntExtra("scale", -1);
                int status = intent.getIntExtra("status", -1);

                int level = -1;
                if(rawlevel >= 0 && scale > 0){
                    level = (rawlevel*100)/scale;
                }
                sb.append("电池电量: ");
                sb.append(level + "%\n");



                String batteryStatus ="";
                switch (status) {
                    case BatteryManager.BATTERY_STATUS_UNKNOWN:
                        batteryStatus="[没有安装电池]";
                        break;
                    case BatteryManager.BATTERY_STATUS_CHARGING:
                        batteryStatus="[正在充电]";
                        break;
                    case BatteryManager.BATTERY_STATUS_FULL:
                        batteryStatus="[已经充满]";
                        break;
                    case BatteryManager.BATTERY_STATUS_DISCHARGING:
                        batteryStatus="[放电中]";
                        break;
                    case BatteryManager.BATTERY_STATUS_NOT_CHARGING:
                        batteryStatus="[未充电]";
                        break;
                    default:
                        if(level <= 10)
                            sb.append("[电量过低，请充电]");
                        else if (level <= 100) {
                            sb.append("[未连接充电器]");
                        }
                        break;

                }
                sb.append(batteryStatus);
//                sb.append("\n");
//                sb.append(getCurrent());


                batterLevel.setText(sb.toString());
            }

        };
        batteryLevelFilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
        registerReceiver(batteryLevelRcvr, batteryLevelFilter);
    }
}