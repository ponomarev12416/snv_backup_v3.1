BEGIN;
--
-- Create model Job
--
CREATE TABLE "backup_job" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL UNIQUE, "status" varchar(50) NOT NULL, "last_run" varchar(200) NOT NULL, "date_created" datetime NOT NULL, "destination" varchar(1350) NOT NULL, "time" time NOT NULL, "MONDAY" bool NOT NULL, "TUESDAY" bool NOT NULL, "WEDNESDAY" bool NOT NULL, "THURSDAY" bool NOT NULL, "FRIDAY" bool NOT NULL, "SATURDAY" bool NOT NULL, "SUNDAY" bool NOT NULL);
--
-- Create model Repository
--
CREATE TABLE "backup_repository" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "path" varchar(750) NOT NULL);
CREATE TABLE "backup_repository_job" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "repository_id" bigint NOT NULL REFERENCES "backup_repository" ("id") DEFERRABLE INITIALLY DEFERRED, "job_id" bigint NOT NULL REFERENCES "backup_job" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "backup_repository_job_repository_id_job_id_5a6250ae_uniq" ON "backup_repository_job" ("repository_id", "job_id");
CREATE INDEX "backup_repository_job_repository_id_a86941de" ON "backup_repository_job" ("repository_id");
CREATE INDEX "backup_repository_job_job_id_a921d484" ON "backup_repository_job" ("job_id");
COMMIT;
