// g++  --std=c++14  pulsar_consume.cpp -lpulsar -o pulsar_consume
#include <pulsar/Client.h>
#include <ctime>
#include <iostream>
#include <unistd.h>
#include <thread>
#include <chrono>

using namespace pulsar;
using namespace std;

void ack(Consumer &consumer, vector<Message> &mvec, int &totalAck) {
    const auto sleepTime = 5s;
    while (true) {
        if (access( "touchfile", F_OK ) == 0) {
            if (mvec.size()>1) {
                for(int i = 0; i < mvec.size()-1 ; i++) {
                    consumer.acknowledge(mvec[i]);
		    mvec.erase(mvec.begin()+i);
                    totalAck++;
                }
                cout <<"ACK - *** Acknowledged all the pending messages ***"<< endl;
            }
        }
        std::this_thread::sleep_for(sleepTime);
    }
}

int main() {
    Client client("pulsar://localhost:6650");
    Consumer consumer;
    ConsumerConfiguration config;
    config.setReceiverQueueSize(100);
    config.setUnAckedMessagesTimeoutMs(10000);
    config.setSubscriptionInitialPosition(InitialPositionEarliest);
    Result result = client.subscribe("persistent://testTenant/ns/testTopic4", "sub-1", config, consumer);
    // if (result != ResultOk) {
    //     std::cout << "Failed to subscribe: " << result << std::endl;
    //     return -1;
    // }
    // while(true) {};

    // vector<Message> mvec;
    Message msg;
    // int totalMessages = 0;
    // int totalAck = 0;
    // time_t start = time(NULL);
    // std::thread ackthread (ack, std::ref(consumer), std::ref(mvec), std::ref(totalAck));
    // ackthread.detach();
    // while (true) {
    //     consumer.receive(msg);

    //     totalMessages++;

	// cout << "Message- Count: " << msg.getRedeliveryCount() << " String: " << msg.getDataAsString() << endl;
    //     mvec.push_back(msg);
    //     if (difftime(time(NULL), start) >=1 ) {
    //         BrokerConsumerStats stats;
    //         consumer.getBrokerConsumerStats(stats);
    //         cout << "Report - Total Messages Received: " << totalMessages
    //              << " Total Acknowledged: " << totalAck
    //              << " UnAcknowledged: " << stats.getUnackedMessages()
    //              << " Backlog Size: " << stats.getMsgBacklog()
    //              << " Is Blocked: " << (stats.isBlockedConsumerOnUnackedMsgs() ? "Yes" : "No")
    //              << " Is Valid: " << (stats.isValid() ? "Yes" : "No") << endl;
    //         start = time(NULL);
    //     }
    // }

    // std::cout << "Finished consuming synchronously!" << std::endl;

    cout<<"Waiting for /tmp/proceed1 file to close the consumer"<<endl;
    while(access("/tmp/proceed1", F_OK) != 0);
    consumer.close();

    cout<<"Waiting for /tmp/proceed2 file to start receving on consumer"<<endl;
    while(access("/tmp/proceed2", F_OK) != 0);

    client.subscribe("persistent://testTenant/ns/testTopic4", "sub-1", config, consumer);

    cout<<"Waiting for /tmp/proceed3 file to stop the client"<<endl;
    while(access("/tmp/proceed3", F_OK) != 0);


    client.close();
    return 0;
}

