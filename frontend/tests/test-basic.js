import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
    stages: [
        {duration: '30s', target: 10},
        {duration: '30s', target: 100},
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],
        http_req_failed: ['rate<0.01'],
    },
};

const BASE_URL = 'http://localhost:8000';

export default function () {
    let res = http.post(`${BASE_URL}/heavy-calculation?iterations=100000&chars_count=50`);
    check(res, {
        'status is 200': (r) => r.status === 200,
        'response time < 300ms': (r) => r.timings.duration < 300,
    });

    sleep(1);

    res = http.get(`${BASE_URL}/health/check`);
    check(res , {
        'health check successful': (r) => r.status === 200,
    });

    sleep(1);
}
