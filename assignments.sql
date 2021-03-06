BEGIN;
--
--

CREATE model Assignment
--

CREATE TABLE "assignments_assignment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "description" text NOT NULL, "published" datetime NOT NULL, "deadline" datetime NOT NULL, "status" varchar(2) NOT NULL);
--
--

CREATE model Submission
--

CREATE TABLE "assignments_submission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "status" varchar(2) NOT NULL, "remark" text NOT NULL, "submission" text NOT NULL, "assignment_id" bigint NOT NULL REFERENCES "assignments_assignment" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "assignments_submission_assignment_id_5322e0a4"
ON "assignments_submission" ("assignment_id"); COMMIT;