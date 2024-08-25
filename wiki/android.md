# Android 开发笔记

## 使用 Log 打印日志

在`app/src/main/java/com/firstActivity.java`输入`logt`回车自动生成 tag 字符串

```java
package com.example.helloworld;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.v(TAG, "onCreate");
    }
}
```

可以在 Logcat 里面查看日志。

## 手动创建 Activity

创建一个新项目，选择 no activity。在源文件目录下的 res 目录下的 layout 文件夹是存放布局的地方，在 layout 文件夹下添加文件 Layout Resource File，命名为 first_layout，在界面添加一个按钮

```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <!--    
        id 设置代码的唯一标识符 
        layout_width 参数 match_parent 表示与父类宽度一样
        layout_height 参数 wrap_content 表示刚好包含文字大小
        text 按钮文本
    -->
    <Button
        android:id="@+id/Button_1"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="button"
        tools:ignore="MissingConstraints" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

下面就需要在活动中加载布局，在 android 中活动与布局是分开的。

在 `app/src/main/java/com/firstActivity.java`输入

```java
package com;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import com.example.firstapplication.R;

public class firstActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.first_layout);
    }
}
```

通过 setContent view 方法给当前活动加载布局，在 setContent 方法中我们需要传入一个布局文件的 ID。项目中的任何资源都会在 R 中生成相应的资源 ID。

最后在 AndroidManifest 文件中进行注册。还需要给程序添加主活动。不然程序不知道先运行哪个活动。