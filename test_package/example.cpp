#include <trantor/utils/ConcurrentTaskQueue.h>
#include <trantor/utils/Logger.h>
#include <iostream>
#include <atomic>
#include <thread>
#include <chrono>
#include <time.h>
#include <stdio.h>
using namespace std::chrono_literals;

void test()
{
    trantor::ConcurrentTaskQueue queue(5, "concurrT");
    std::atomic_int sum;
    sum = 0;
    for (int i = 0; i < 4; ++i)
    {
        queue.runTaskInQueue([&sum]() {
            LOG_DEBUG << "add sum";
            for (int i = 0; i < 10000; ++i)
            {
                ++sum;
            }
        });
    }

    queue.runTaskInQueue([&sum]() {
        for (int i = 0; i < 5; ++i)
        {
            LOG_DEBUG << "sum=" << sum;
            std::this_thread::sleep_for(100us);
        }
    });

    LOG_DEBUG << "sum=" << sum;
}

int main() {
    test();

    std::cout << "Trantor ok." << std::endl;
    return 0;
}
