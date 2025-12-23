import { createORM } from "pinia-orm";
import { Language } from "./language.js";
import { Domain } from "./domain.js";
import { MasterWord } from "./masterWord.js";
import { Translation } from "./translation.js";
import { User } from "./user.js";
import { SessionConfig } from "./sessionConfig.js";
import { Session } from "./session.js";
import { SessionResult } from "./sessionResult.js";
import { UserProgress } from "./userProgress.js";

// Create ORM instance and register models
export const orm = createORM({
  models: [
    Language,
    Domain,
    MasterWord,
    Translation,
    User,
    SessionConfig,
    Session,
    SessionResult,
    UserProgress
  ],
});

export {
  Language,
  Domain,
  MasterWord,
  Translation,
  User,
  SessionConfig,
  Session,
  SessionResult,
  UserProgress
};
