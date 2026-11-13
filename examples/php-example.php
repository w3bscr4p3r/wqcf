<?php
require __DIR__ . '/../sdk/php/src/Client.php';
$client = new Wqcf\Client('http://127.0.0.1:8080');
print_r($client->health());
print_r($client->capabilities());
