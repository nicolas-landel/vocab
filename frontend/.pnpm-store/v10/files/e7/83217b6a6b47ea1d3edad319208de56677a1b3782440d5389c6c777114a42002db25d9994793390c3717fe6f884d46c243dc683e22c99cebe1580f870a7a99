class EntitySchema {
  constructor(key, definition = {}, options = {}) {
    if (!key || typeof key !== "string") {
      throw new Error(`Expected a string key for Entity, but found ${key}.`);
    }
    const {
      idAttribute = "id",
      mergeStrategy = (entityA, entityB) => {
        return { ...entityA, ...entityB };
      },
      processStrategy = (input) => ({ ...input })
    } = options;
    this._key = key;
    this._getId = idAttribute;
    this._mergeStrategy = mergeStrategy;
    this._processStrategy = processStrategy;
    this.define(definition);
  }
  get key() {
    return this._key;
  }
  define(definition) {
    this.schema = Object.keys(definition).reduce((entitySchema, key) => {
      const schema = definition[key];
      return { ...entitySchema, [key]: schema };
    }, this.schema || {});
  }
  getId(input, parent, key) {
    return this._getId(input, parent, key);
  }
  merge(entityA, entityB) {
    return this._mergeStrategy(entityA, entityB);
  }
  normalize(input, parent, key, visit, addEntity, visitedEntities) {
    const id = this.getId(input, parent, key);
    const entityType = this.key;
    if (!(entityType in visitedEntities)) {
      visitedEntities[entityType] = {};
    }
    if (!(id in visitedEntities[entityType])) {
      visitedEntities[entityType][id] = [];
    }
    if (visitedEntities[entityType][id].includes(input)) {
      return id;
    }
    visitedEntities[entityType][id].push(input);
    const processedEntity = this._processStrategy(input, parent, key);
    Object.keys(this.schema).forEach((key2) => {
      if (processedEntity.hasOwnProperty(key2) && typeof processedEntity[key2] === "object") {
        const schema = this.schema[key2];
        const resolvedSchema = typeof schema === "function" ? schema(input) : schema;
        processedEntity[key2] = visit(
          processedEntity[key2],
          processedEntity,
          key2,
          resolvedSchema,
          addEntity,
          visitedEntities
        );
      }
    });
    addEntity(this, processedEntity, input, parent, key);
    return id;
  }
}

class PolymorphicSchema {
  constructor(definition, schemaAttribute) {
    if (schemaAttribute) {
      this._schemaAttribute = typeof schemaAttribute === "string" ? (input) => input[schemaAttribute] : schemaAttribute;
    }
    this.define(definition);
  }
  get isSingleSchema() {
    return !this._schemaAttribute;
  }
  define(definition) {
    this.schema = definition;
  }
  getSchemaAttribute(input, parent, key) {
    return !this.isSingleSchema && this._schemaAttribute(input, parent, key);
  }
  inferSchema(input, parent, key) {
    if (this.isSingleSchema) {
      return this.schema;
    }
    const attr = this.getSchemaAttribute(input, parent, key);
    return this.schema[attr];
  }
  normalizeValue(value, parent, key, visit, addEntity, visitedEntities) {
    const schema = this.inferSchema(value, parent, key);
    if (!schema) {
      return value;
    }
    const normalizedValue = visit(value, parent, key, schema, addEntity, visitedEntities);
    return this.isSingleSchema || normalizedValue === void 0 || normalizedValue === null ? normalizedValue : { id: normalizedValue, schema: this.getSchemaAttribute(value, parent, key) };
  }
}

class UnionSchema extends PolymorphicSchema {
  constructor(definition, schemaAttribute) {
    if (!schemaAttribute) {
      throw new Error('Expected option "schemaAttribute" not found on UnionSchema.');
    }
    super(definition, schemaAttribute);
  }
  normalize(input, parent, key, visit, addEntity, visitedEntities) {
    return this.normalizeValue(input, parent, key, visit, addEntity, visitedEntities);
  }
}

const validateSchema = (definition) => {
  if (Array.isArray(definition) && definition.length > 1) {
    throw new Error(`Expected schema definition to be a single schema, but found ${definition.length}.`);
  }
  return definition[0];
};
const getValues = (input) => Array.isArray(input) ? input : Object.keys(input).map((key) => input[key]);
const normalize$2 = (schema, input, parent, key, visit, addEntity, visitedEntities) => {
  return getValues(input).map((value) => visit(value, parent, key, validateSchema(schema), addEntity, visitedEntities));
};
class ArraySchema extends PolymorphicSchema {
  normalize(input, parent, key, visit, addEntity, visitedEntities) {
    return getValues(input).map((value) => this.normalizeValue(value, parent, key, visit, addEntity, visitedEntities)).filter((value) => value !== void 0 && value !== null);
  }
}

const normalize$1 = (schema, input, parent, key, visit, addEntity, visitedEntities) => {
  const object = { ...input };
  Object.keys(schema).forEach((key2) => {
    const localSchema = schema[key2];
    const resolvedLocalSchema = typeof localSchema === "function" ? localSchema(input) : localSchema;
    const value = visit(input[key2], input, key2, resolvedLocalSchema, addEntity, visitedEntities);
    if (value === void 0 || value === null) {
      delete object[key2];
    } else {
      object[key2] = value;
    }
  });
  return object;
};

const visit = (value, parent, key, schema2, addEntity, visitedEntities) => {
  if (typeof value !== "object" || !value) {
    return value;
  }
  if (typeof schema2 === "object" && (!schema2.normalize || typeof schema2.normalize !== "function")) {
    const method = Array.isArray(schema2) ? normalize$2 : normalize$1;
    return method(schema2, value, parent, key, visit, addEntity, visitedEntities);
  }
  return schema2.normalize(value, parent, key, visit, addEntity, visitedEntities);
};
const addEntities = (entities) => (schema2, processedEntity, value, parent, key) => {
  const schemaKey = schema2.key;
  const id = schema2.getId(value, parent, key);
  if (!(schemaKey in entities)) {
    entities[schemaKey] = {};
  }
  entities[schemaKey][id] = entities[schemaKey][id] ? schema2.merge(entities[schemaKey][id], processedEntity) : processedEntity;
};
const schema = {
  Array: ArraySchema,
  Entity: EntitySchema,
  Union: UnionSchema
};
const normalize = (input, schema2) => {
  if (!input || typeof input !== "object") {
    throw new Error(
      `Unexpected input given to normalize. Expected type to be "object", found "${input === null ? "null" : typeof input}".`
    );
  }
  const entities = {};
  const addEntity = addEntities(entities);
  const visitedEntities = {};
  const result = visit(input, input, null, schema2, addEntity, visitedEntities);
  return { entities, result };
};

export { normalize, schema };
