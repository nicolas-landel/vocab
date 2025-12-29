import { createORM } from "pinia-orm";
import { Language } from "./language.js";
import { Domain } from "./domain.js";
import { MasterWord } from "./masterWord.js";
import { Translation } from "./translation.js";
import { User } from "./user.js";
import { SessionConfig } from "./sessionConfig.js";
import { Session } from "./session.js";
import { SessionWord } from "./sessionWord.js";
import { UserProgress } from "./userProgress.js";
import { UserLanguage } from "./userLanguage.js";

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
    SessionWord,
    UserProgress,
    UserLanguage
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
  SessionWord,
  UserProgress,
  UserLanguage
};
