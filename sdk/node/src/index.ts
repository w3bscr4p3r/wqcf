export type WqcfOptions = { token?: string; timeoutMs?: number };

export class WqcfClient {
  constructor(private readonly baseUrl: string, private readonly options: WqcfOptions = {}) {}

  health() { return this.request<{status: string}>("GET", "/health"); }
  capabilities() { return this.request<Record<string, unknown>>("GET", "/v1/capabilities"); }

  verifyMlDsa65(message_b64: string, signature_b64: string, public_key_b64: string) {
    return this.request<{algorithm: string; valid: boolean}>(
      "POST", "/v1/signatures/ml-dsa-65/verify",
      { algorithm: "ML-DSA-65", message_b64, signature_b64, public_key_b64 }
    );
  }

  private async request<T>(method: string, path: string, body?: unknown): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.options.timeoutMs ?? 10000);
    try {
      const response = await fetch(new URL(path, this.baseUrl), {
        method, signal: controller.signal,
        headers: {
          "content-type": "application/json",
          ...(this.options.token ? { authorization: `Bearer ${this.options.token}` } : {})
        },
        ...(body === undefined ? {} : { body: JSON.stringify(body) })
      });
      const data = await response.json() as any;
      if (!response.ok) throw new Error(data?.detail ?? `WQCF HTTP ${response.status}`);
      return data as T;
    } finally { clearTimeout(timeout); }
  }
}
