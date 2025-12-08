
export function toSnakeCase(str) {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}
export function toCamelCase(str) {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}
export function transformObjectToSnakeCase(obj) {
  if (obj === null || typeof obj !== "object") return obj;
  if (Array.isArray(obj)) {
    return obj.map(transformObjectToSnakeCase);
  }
  const transformed = {};
  for (const [key, value] of Object.entries(obj)) {
    const snakeKey = toSnakeCase(key);
    transformed[snakeKey] =
      typeof value === "object" ? transformObjectToSnakeCase(value) : value;
  }
  return transformed;
}
export function transformObjectToCamelCase(obj) {
  if (obj === null || typeof obj !== "object") return obj;
  if (Array.isArray(obj)) {
    return obj.map(transformObjectToCamelCase);
  }
  const transformed = {};
  for (const [key, value] of Object.entries(obj)) {
    const camelKey = toCamelCase(key);
    transformed[camelKey] =
      typeof value === "object" ? transformObjectToCamelCase(value) : value;
  }
  return transformed;
}