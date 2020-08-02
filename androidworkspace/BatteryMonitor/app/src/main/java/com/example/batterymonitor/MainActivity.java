package com.example.batterymonitor;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.BatteryManager;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    private TextView batterLevel;
    private BroadcastReceiver batteryLevelRcvr;
    private IntentFilter batteryLevelFilter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        batterLevel = (TextView)findViewById(R.id.batteryLevel);
        monitorBatteryState();
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
                int health = intent.getIntExtra("health", -1);
                int level = -1;
                if(rawlevel >= 0 && scale > 0){
                    level = (rawlevel*100)/scale;
                }
                sb.append("电池电量: ");
                sb.append(level + "%\n");

                String healthStatus = "";
                switch (health) {
                    case BatteryManager.BATTERY_HEALTH_UNKNOWN:
                        healthStatus = "UNKNOWN";
                        break;
                    case BatteryManager.BATTERY_HEALTH_GOOD:
                        healthStatus = "GOOD";
                        break;
                    case BatteryManager.BATTERY_HEALTH_OVERHEAT:
                        healthStatus = "OVERHEAT";
                        break;
                    case BatteryManager.BATTERY_HEALTH_DEAD:
                        healthStatus = "DEAD";
                        break;
                    case BatteryManager.BATTERY_HEALTH_OVER_VOLTAGE:
                        healthStatus = "OVER VOLTAGE";
                        break;
                    case BatteryManager.BATTERY_HEALTH_UNSPECIFIED_FAILURE:
                        healthStatus = "UNSPECIFIED FAILURE";
                        break;
                    case BatteryManager.BATTERY_HEALTH_COLD:
                        healthStatus = "COLD";
                        break;

                }
                sb.append("健康度:" + healthStatus + "\n");

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

                batterLevel.setText(sb.toString());
            }

        };
        batteryLevelFilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
        registerReceiver(batteryLevelRcvr, batteryLevelFilter);
    }
}