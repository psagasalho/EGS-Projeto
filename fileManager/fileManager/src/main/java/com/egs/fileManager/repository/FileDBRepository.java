package com.egs.fileManager.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.egs.fileManager.model.FileDB;

@Repository
public interface FileDBRepository extends JpaRepository<FileDB, String> {

}