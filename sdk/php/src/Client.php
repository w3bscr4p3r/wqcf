<?php
declare(strict_types=1);
namespace Wqcf;

final class Client
{
    public function __construct(
        private readonly string $baseUrl,
        private readonly ?string $token = null,
        private readonly int $timeout = 10
    ) {}

    public function capabilities(): array { return $this->request('GET', '/v1/capabilities'); }
    public function health(): array { return $this->request('GET', '/health'); }

    public function verifyMlDsa65(string $messageB64, string $signatureB64, string $publicKeyB64): array
    {
        return $this->request('POST', '/v1/signatures/ml-dsa-65/verify', [
            'algorithm' => 'ML-DSA-65',
            'message_b64' => $messageB64,
            'signature_b64' => $signatureB64,
            'public_key_b64' => $publicKeyB64,
        ]);
    }

    private function request(string $method, string $path, ?array $body = null): array
    {
        $headers = ["Content-Type: application/json"];
        if ($this->token !== null) $headers[] = "Authorization: Bearer {$this->token}";
        $ch = curl_init(rtrim($this->baseUrl, '/') . $path);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true, CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => $headers, CURLOPT_TIMEOUT => $this->timeout,
        ]);
        if ($body !== null) curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body, JSON_THROW_ON_ERROR));
        $raw = curl_exec($ch);
        if ($raw === false) { $error = curl_error($ch); curl_close($ch); throw new \RuntimeException($error); }
        $status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);
        $data = json_decode($raw, true);
        if (!is_array($data)) throw new \RuntimeException("Invalid WQCF response");
        if ($status >= 400) throw new \RuntimeException($data['detail'] ?? "WQCF HTTP {$status}");
        return $data;
    }
}
