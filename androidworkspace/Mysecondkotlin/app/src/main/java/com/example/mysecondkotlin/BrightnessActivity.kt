package com.example.mysecondkotlin

import android.app.Activity
import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.util.Log
import android.view.View
import android.widget.SeekBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_brightness.*
import java.util.*
import kotlin.concurrent.schedule
private const val RQ_WRITE_SETTINGS = 100
class BrightnessActivity : AppCompatActivity() {
    protected lateinit var mContext: Context
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_brightness)

        tvWindowBright.text = "当前窗口亮度=$windowBrightness"
        sbWindowBright.progress = if (windowBrightness > 0) (windowBrightness * 100).toInt() else 0
        sbWindowBright.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                windowBrightness = progress.toFloat() / 100F
                tvWindowBright.text = "当前窗口亮度=$windowBrightness"
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
            }

        })
        Bright_atuodown.setOnClickListener(object : View.OnClickListener {
            override fun onClick(v: View?) {

                Toast.makeText(v?.context, "brihtdownclick", Toast.LENGTH_SHORT).show();
                //brightdown()
                while (windowBrightness > 0.1F) {

                    Log.d(this@BrightnessActivity.toString(), windowBrightness.toString())
                    tvWindowBright.text = "当前窗口亮度=$windowBrightness"


//                    Timer().schedule(1000){
//                        Log.d(this@BrightnessActivity.toString(), tvWindowBright.text .toString())
//                        windowBrightness -= 0.1F
//                    }

                    try {
                        Thread.sleep(500)
                        Log.d(this@BrightnessActivity.toString(), tvWindowBright.text .toString())
                        windowBrightness -= 0.1F
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }

                    sbWindowBright.progress = (windowBrightness * 100).toInt()
                }
                if (windowBrightness > 0.0F && windowBrightness <= 0.1F){
                    windowBrightness = 0F
                    tvWindowBright.text = "当前窗口亮度=$windowBrightness"
                    sbWindowBright.progress = (windowBrightness * 100).toInt()}
            }
        })

    }

    fun brightdownstep(){
        if (windowBrightness >=  0.0F && windowBrightness < 0.1F)
            windowBrightness = 0F
        else  windowBrightness -= 0.1F
    }
    var Activity.windowBrightness
        get() = window.attributes.screenBrightness
        set(brightness) {
            //小于0或大于1.0默认为系统亮度
            window.attributes = window.attributes.apply {
                screenBrightness = if (brightness > 1.0 || brightness < 0) -1.0F else brightness
            }
        }
}

