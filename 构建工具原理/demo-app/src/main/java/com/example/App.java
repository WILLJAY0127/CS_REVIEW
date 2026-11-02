package com.example;

import org.apache.commons.io.FileUtils;
import java.io.File;
import java.io.IOException;

/**
 * 演示 Maven 项目的主类
 */
public class App {
    public static void main(String[] args) throws IOException {
        System.out.println("Hello, Maven World!");
        
        // 用了 commons-io（传递依赖会被自动拉进来）
        String tempDir = System.getProperty("java.io.tmpdir");
        long size = FileUtils.sizeOfDirectory(new File(tempDir));
        System.out.println("Temp dir size: " + size + " bytes");
    }
}
