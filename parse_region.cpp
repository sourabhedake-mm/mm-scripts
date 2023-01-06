#include<iostream>
using namespace std;
std::string parse(std::string cluster) {
  size_t firstHypen = cluster.rfind('-');
  if (firstHypen == cluster.npos) {
    return cluster; // return as it is
  }
  size_t secondHypen = cluster.rfind('-', firstHypen - 1);
  if (secondHypen == cluster.npos) {
    return cluster.substr(firstHypen + 1); // one-word region name
  }
  return cluster.substr(secondHypen + 1);  // two-word region name
}

int main() {
	cout << parse("sourabh") << endl;
	cout << parse("sourabh-ap") <<endl;
	cout << parse("sourabh-ap-west") <<endl;
	cout << parse("sourabh-ok-ap-west") <<endl;
	cout << parse("") <<endl;
	return 0;
}
