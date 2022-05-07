package com.egs.fileManager;

import javax.annotation.Resource;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import com.egs.fileManager.uploadDownload.service.FileStorageService;


@SpringBootApplication
public class FileManagerApplication implements CommandLineRunner {
	@Resource
	FileStorageService storageService;
	public static void main(String[] args) {
		SpringApplication.run(FileManagerApplication.class, args);
	}
	@Override
	public void run(String... arg) throws Exception {
		storageService.deleteAll();
		storageService.init();
	}
}
