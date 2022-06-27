BEGIN;
--
-- Create model Job
--
CREATE TABLE "backup_job" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(200) NOT NULL, 
    "status" varchar(50) NOT NULL, 
    "last_run" varchar(200) NOT NULL, 
    "date_created" datetime NOT NULL, 
    "destination" varchar(1350) NOT NULL);
--
-- Create model Schedule
--
CREATE TABLE "backup_schedule" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "time" time NOT NULL, 
    "MONDAY" bool NOT NULL, 
    "TUESDAY" bool NOT NULL, 
    "WEDNESDAY" bool NOT NULL, 
    "THURSDAY" bool NOT NULL, 
    "FRIDAY" bool NOT NULL, 
    "SATURDAY" bool NOT NULL, 
    "SUNDAY" bool NOT NULL, 
    "job_id" bigint NOT NULL UNIQUE REFERENCES "backup_job" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Repositories
--
CREATE TABLE "backup_repositories" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "path" varchar(750) NOT NULL);
    
CREATE TABLE "backup_repositories_job" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "repositories_id" bigint NOT NULL REFERENCES "backup_repositories" ("id") DEFERRABLE INITIALLY DEFERRED, 
    "job_id" bigint NOT NULL REFERENCES "backup_job" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE UNIQUE INDEX "backup_repositories_job_repositories_id_job_id_e84e80ee_uniq" 
ON "backup_repositories_job" ("repositories_id", "job_id");

CREATE INDEX "backup_repositories_job_repositories_id_9e682594" 
ON "backup_repositories_job" ("repositories_id");

CREATE INDEX "backup_repositories_job_job_id_8315e157" 
ON "backup_repositories_job" ("job_id");
COMMIT;
