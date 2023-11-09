export const isObjectMatchingStructure = (obj) => {
  // Check if obj is an object
  if (typeof obj !== 'object' || obj === null) {
    return false;
  }

  // Check if obj has a "title" property
  if (!obj.hasOwnProperty('title')) {
    return false;
  }

  // Check if obj has a "type" property that is an object
  if (typeof obj.type !== 'object' || obj.type === null) {
    return false;
  }

  // Check if the "type" object has a "name" property
  if (!obj.type.hasOwnProperty('name')) {
    return false;
  }

  // Check if the "type" object has an "isWordLevel" property of type boolean
  if (typeof obj.type.isWordLevel !== 'boolean') {
    return false;
  }

  // Check if obj has an "output_index" property
  if (!obj.hasOwnProperty('output_index')) {
    return false;
  }

  // Check if obj has an "input_index" property
  if (!obj.hasOwnProperty('input_index')) {
    return false;
  }

  // Check if obj has a "labels" property that is an array
  if (!Array.isArray(obj.labels)) {
    return false;
  }

  // Check if obj has an "id" property
  if (!obj.hasOwnProperty('id')) {
    return false;
  }

  // If all checks pass, the object matches the structure
  return true;
}
