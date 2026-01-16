import { randomUUID } from "crypto";

/**
 * Genera una API Key única usando UUID v4
 * @returns {string} UUID único
 */
export function generateApiKey() {
  return randomUUID();
}
