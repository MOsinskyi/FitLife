import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '30s', target: 10 },   // Ramp up to 10 users
        { duration: '1m', target: 50 },    // Ramp up to 50 users
        { duration: '30s', target: 0 },    // Ramp down to 0 users
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],  // 95% of requests should be below 500ms
        http_req_failed: ['rate<0.01'],    // Less than 1% of requests should fail
    },
};

const BASE_URL = 'http://localhost:8000/api/v1';

// Test data
const testMember = {
    first_name: 'Test',
    last_name: 'User',
    email: `test${Date.now()}@gym.ua`,
    phone_number: '+380671234567',
    password: 'password123',
};

const testCoach = {
    first_name: 'Coach',
    last_name: 'Test',
    email: `coach${Date.now()}@gym.ua`,
    phone_number: '+380501234567',
    password: 'password123',
    specialization: 'Yoga',
    experience: 5,
};

export default function () {
    // Test 1: Register a new member
    let res = http.post(
        `${BASE_URL}/members/`,
        JSON.stringify({
            ...testMember,
            email: `member${__VU}_${__ITER}@gym.ua`, // Unique email per virtual user and iteration
        }),
        {
            headers: { 'Content-Type': 'application/json' },
        }
    );
    check(res, {
        'member registration successful': (r) => r.status === 201,
        'member registration response time < 300ms': (r) => r.timings.duration < 300,
    });

    sleep(1);

    // Test 2: Login as member
    res = http.post(
        `${BASE_URL}/auth/login`,
        JSON.stringify({
            username: `member${__VU}_${__ITER}@gym.ua`,
            password: 'password123',
        }),
        {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        }
    );
    check(res, {
        'member login successful': (r) => r.status === 200,
    });

    const memberToken = res.json('access_token');

    sleep(1);

    // Test 3: Get all coaches (as authenticated member)
    res = http.get(`${BASE_URL}/coaches`, {
        headers: {
            'Authorization': `Bearer ${memberToken}`,
        },
    });
    check(res, {
        'get coaches successful': (r) => r.status === 200,
        'coaches list is array': (r) => Array.isArray(r.json()),
    });

    sleep(1);

    // Test 4: Get all training sessions
    res = http.get(`${BASE_URL}/training-sessions`, {
        headers: {
            'Authorization': `Bearer ${memberToken}`,
        },
    });
    check(res, {
        'get training sessions successful': (r) => r.status === 200,
        'training sessions response time < 200ms': (r) => r.timings.duration < 200,
    });

    sleep(1);
}

// Setup function - runs once at the beginning
export function setup() {
    console.log('Starting load test for FitLife API');
    return { timestamp: new Date().toISOString() };
}

// Teardown function - runs once at the end
export function teardown(data) {
    console.log(`Load test completed at ${new Date().toISOString()}`);
    console.log(`Test started at ${data.timestamp}`);
}
