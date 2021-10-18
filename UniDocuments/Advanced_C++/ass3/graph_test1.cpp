#include "gdwg/graph.hpp"

#include <catch2/catch.hpp>
#include <fmt/format.h>
#include <fmt/ostream.h>
#include <iostream>
#include <sstream>
#include <string>

/*
// z5185797 Yuta Sato

Test description
This test is implemented to cover all the cases in spec.
For this, included all different constructors test case and types
such as string, int, char, double implemented by template type.
Not only constructors , I include constructor, operation, method, friend, iterator as well.
I tried to use many test case and section this time, since I can write comment for each test
and improve clearity.
The order of test case is followed by spec order.
*/

// Constructors
TEST_CASE("Default Constructor") {
	SECTION("Make graph without contents") {
		auto out = std::ostringstream{};
		gdwg::graph<int, double> g;
		out << g;
		REQUIRE(out.str().empty());
	}
}

TEST_CASE("Creating an empty graph with std::vector iterators") {
	std::ostringstream oss;
	SECTION("vector of strings") {
		std::vector<std::string> v{"Hello", "how", "are", "you"};
		gdwg::graph<std::string, double> g{v.begin(), v.end()};
		oss << g;
		REQUIRE(oss.str() == "Hello (\n)\nare (\n)\nhow (\n)\nyou (\n)\n");
	}

	SECTION("A Vector of ints") {
		std::vector<int> v{3, 6, 2, 1};
		gdwg::graph<int, double> g{v.begin(), v.end()};
		oss << g;
		REQUIRE(oss.str() == "1 (\n)\n2 (\n)\n3 (\n)\n6 (\n)\n");
	}
}

TEST_CASE("Other Constructors ") {
	std::ostringstream oss;
	SECTION("graph with nodes and edges") {
		using graph = gdwg::graph<int, int>;
		auto const v = std::vector<graph::value_type>{
		   {1, 2, 2},
		   {1, 3, 2},
		   {2, 3, 1},
		};
		auto g = graph(v.begin(), v.end());
		auto nodes = g.nodes();
		REQUIRE(nodes.size() == 3);
		REQUIRE(g.is_node(1));
		REQUIRE(g.is_node(2));
		REQUIRE(g.is_node(3));
	}

	SECTION("graph with only strings") {
		gdwg::graph<char, std::string> g{'a', 'b', 'x', 'y'};
		oss << g;
		REQUIRE(oss.str() == "a (\n)\nb (\n)\nx (\n)\ny (\n)\n");
	}

	SECTION("graph with initializer list") {
		std::initializer_list<char> node_chars{'a', 'b'};
		gdwg::graph<char, std::string> g{node_chars};
		auto nodes = g.nodes();
		REQUIRE(nodes.size() == 2);
		REQUIRE(g.is_node('a'));
		REQUIRE(g.is_node('b'));
	}
}

TEST_CASE("Copy and Move Constructors") {
	gdwg::graph<std::string, int> g;
	g.insert_node("a");
	g.insert_node("b");
	g.insert_node("c");
	g.insert_node("d");
	g.insert_edge("a", "b", 1);
	g.insert_edge("a", "c", 2);
	g.insert_edge("a", "d", 3);

	SECTION("Copy") {
		auto copy{g};
		REQUIRE(copy.nodes() == g.nodes());
		REQUIRE(copy.connections("a") == g.connections("a"));
		REQUIRE(copy.connections("b") == g.connections("b"));
		REQUIRE(copy.connections("c") == g.connections("c"));
		REQUIRE(copy.connections("d") == g.connections("d"));
		REQUIRE(copy == g);
	}

	SECTION("Move") {
		auto copy{std::move(g)};
		std::vector<std::string> a_neighbours = {"b", "c", "d"};
		std::vector<std::string> all_nodes = {"a", "b", "c", "d"};

		REQUIRE(copy.nodes() == all_nodes);
		REQUIRE(copy.connections("a") == a_neighbours);
		REQUIRE(copy.connections("b").empty());
		REQUIRE(copy.connections("c").empty());
		REQUIRE(copy.connections("d").empty());
	}
}

TEST_CASE("Copy and Move Assignments") {
	gdwg::graph<std::string, int> g;
	g.insert_node("a");
	g.insert_node("b");
	g.insert_node("c");
	g.insert_node("d");
	g.insert_edge("a", "b", 1);
	g.insert_edge("a", "c", 2);
	g.insert_edge("a", "d", 3);

	SECTION("Copy") {
		auto copy = g;
		REQUIRE(copy.nodes() == g.nodes());
		REQUIRE(copy.connections("a") == g.connections("a"));
		REQUIRE(copy.connections("b") == g.connections("b"));
		REQUIRE(copy.connections("c") == g.connections("c"));
		REQUIRE(copy.connections("d") == g.connections("d"));
		REQUIRE(copy == g);
	}

	SECTION("Move") {
		auto copy = std::move(g);
		std::vector<std::string> a_neighbours = {"b", "c", "d"};
		std::vector<std::string> all_nodes = {"a", "b", "c", "d"};

		REQUIRE(copy.nodes() == all_nodes);
		REQUIRE(copy.connections("a") == a_neighbours);
		REQUIRE(copy.connections("b").empty());
		REQUIRE(copy.connections("c").empty());
		REQUIRE(copy.connections("d").empty());
	}
}

// Modifiers
TEST_CASE("Test insert_node() ") {
	gdwg::graph<std::string, int> g;
	g.insert_node("hello");
	g.insert_node("how");
	g.insert_node("are");

	SECTION("return true") {
		REQUIRE(g.is_node("hello") == 1);
		REQUIRE(g.is_node("how") == 1);
	}
	SECTION("return false") {
		REQUIRE(g.is_node("ku") == 0);
		REQUIRE(g.is_node("so") == 0);
	}
}

TEST_CASE("Test insert_edge() ") {
	gdwg::graph<std::string, int> g;
	g.insert_node("hello");
	g.insert_node("how");
	g.insert_node("are");
	g.insert_edge("hello", "how", 5);
	g.insert_edge("how", "are", 7);

	SECTION("return true") {
		REQUIRE(g.is_connected("hello", "how"));
		REQUIRE(g.is_connected("how", "are"));
	}
	SECTION("return false") {
		REQUIRE(g.is_node("un") == 0);
		REQUIRE(g.is_node("choo") == 0);
	}
	SECTION("insert_edge exception") {
		REQUIRE_THROWS_WITH(g.insert_edge("f", "c", 9),
		                    "Cannot call gdwg::graph<N, E>::insert_edge when either src "
		                    "or dst node does not exist");
	}
}

TEST_CASE("More Inserting, Deleting and Replacing Nodes") {
	std::ostringstream oss_1;
	std::ostringstream oss_2;
	SECTION("An graph 'a' with nodes and edges") {
		using graph = gdwg::graph<std::string, int>;
		auto const v = std::vector<graph::value_type>{
		   {"A", "B", 1},
		   {"A", "C", 2},
		   {"A", "D", 3},
		};
		gdwg::graph<std::string, int> a{v.begin(), v.end()};
		oss_1 << a;
		SECTION("Add new node") {
			a.insert_node("E");
			oss_2 << a;
			REQUIRE(oss_1.str() != oss_2.str());
			REQUIRE(oss_2.str() == "A (\n  B | 1\n  C | 2\n  D | 3\n)\nB (\n)\nC (\n)\nD (\n)\nE (\n)\n");
		}

		SECTION("Delete exisiting node") {
			a.erase_node("C");
			oss_2 << a;
			REQUIRE(oss_1.str() != oss_2.str());
			REQUIRE(oss_2.str() == "A (\n  B | 1\n  D | 3\n)\nB (\n)\nD (\n)\n");
		}

		SECTION("Delete non-existing node (no change)") {
			a.erase_node("E");
			oss_2 << a;
			REQUIRE(oss_1.str() == oss_2.str());
			REQUIRE(oss_2.str() == "A (\n  B | 1\n  C | 2\n  D | 3\n)\nB (\n)\nC (\n)\nD (\n)\n");
		}

		SECTION("replace_node node 'E' (non-exisitng) with 'B' (exisitng) with error") {
			REQUIRE_THROWS_WITH(a.replace_node("E", "B"),
			                    "Cannot call gdwg::graph<N, E>::replace_node on a node"
			                    "that doesn't exist");
		}

		SECTION("replace_node node 'A'  with 'B' (exisitng) (no change)") {
			a.replace_node("A", "B");
			oss_2 << a;
			REQUIRE(oss_1.str() == oss_2.str());
		}
	}
}

TEST_CASE("Merge replace test") {
	SECTION("Normall Merge test") {
		auto g = gdwg::graph<std::string, int>{};
		g.insert_node("A");
		g.insert_node("B");
		g.insert_node("C");
		g.insert_node("D");
		g.insert_edge("A", "B", 1);
		g.insert_edge("A", "C", 2);
		g.insert_edge("A", "D", 3);
		g.merge_replace_node("A", "B");

		REQUIRE(g.is_connected("B", "B"));
		REQUIRE(g.is_connected("B", "C"));
		REQUIRE(g.is_connected("B", "D"));
		std::vector<int> weight_to_b{1};
		std::vector<int> weight_to_c{2};
		std::vector<int> weight_to_d{3};
		REQUIRE(g.weights("B", "B") == weight_to_b);
		REQUIRE(g.weights("B", "C") == weight_to_c);
		REQUIRE(g.weights("B", "D") == weight_to_d);
		REQUIRE(!g.is_node("A"));
		g.clear();
		REQUIRE(g.empty());
	}

	SECTION("More Merge test !") {
		auto g = gdwg::graph<std::string, int>{};
		g.insert_node("A");
		g.insert_node("B");
		g.insert_node("C");
		g.insert_node("D");
		g.insert_edge("A", "B", 1);
		g.insert_edge("A", "C", 2);
		g.insert_edge("A", "D", 3);
		g.insert_edge("B", "B", 1);

		g.merge_replace_node("A", "B");
		std::vector<std::string> nodes = {"B", "C", "D"};
		REQUIRE(g.connections("B") == nodes);
		REQUIRE(g.is_connected("B", "B"));
		REQUIRE(g.is_connected("B", "C"));
		REQUIRE(g.is_connected("B", "D"));
		std::vector<int> weight_to_b{1};
		std::vector<int> weight_to_c{2};
		std::vector<int> weight_to_d{3};
		REQUIRE(g.weights("B", "B") == weight_to_b);
		REQUIRE(g.weights("B", "C") == weight_to_c);
		REQUIRE(g.weights("B", "D") == weight_to_d);
		REQUIRE(!g.is_node("A"));
		g.clear();
		REQUIRE(g.empty());
	}

	SECTION("More More Merge test !") {
		auto g = gdwg::graph<std::string, int>{};
		g.insert_node("A");
		g.insert_node("B");
		g.insert_node("C");
		g.insert_node("D");
		g.insert_edge("B", "A", 3);
		g.insert_edge("B", "C", 2);
		g.insert_edge("B", "D", 4);

		g.merge_replace_node("B", "A");
		std::vector<std::string> nodes = {"A", "C", "D"};
		REQUIRE(g.connections("A") == nodes);
		REQUIRE(g.is_connected("A", "A"));
		REQUIRE(g.is_connected("A", "C"));
		REQUIRE(g.is_connected("A", "D"));
		std::vector<int> weight_to_b{3};
		std::vector<int> weight_to_c{2};
		std::vector<int> weight_to_d{4};
		REQUIRE(g.weights("A", "A") == weight_to_b);
		REQUIRE(g.weights("A", "C") == weight_to_c);
		REQUIRE(g.weights("A", "D") == weight_to_d);
	}

	SECTION("More More Merge test !") {
		auto g = gdwg::graph<std::string, int>{};
		g.insert_node("A");
		g.insert_node("B");
		g.insert_node("C");
		g.insert_node("D");
		g.insert_edge("A", "B", 3);
		g.insert_edge("A", "C", 2);
		g.insert_edge("A", "D", 4);

		g.merge_replace_node("A", "B");
		REQUIRE_THROWS_WITH(g.merge_replace_node("t", "b"),
		                    "Cannot call gdwg::graph<N, E>::merge_replace_node on old "
		                    "or new data if they don't exist in the graph");
		REQUIRE_THROWS_WITH(g.merge_replace_node("b", "t"),
		                    "Cannot call gdwg::graph<N, E>::merge_replace_node on old "
		                    "or new data if they don't exist in the graph");
		REQUIRE_THROWS_WITH(g.merge_replace_node("y", "z"),
		                    "Cannot call gdwg::graph<N, E>::merge_replace_node on old "
		                    "or new data if they don't exist in the graph");
	}
}

TEST_CASE("Erase edge test") {
	SECTION("g has three nodes {A,B,C} and 2 edges") {
		gdwg::graph<std::string, int> g;
		g.insert_node("A");
		g.insert_node("B");
		g.insert_node("C");
		g.insert_edge("A", "B", 1);
		g.insert_edge("A", "C", 2);
		SECTION("return true") {
			REQUIRE(g.erase_edge("A", "B", 1) == true);
			std::ostringstream oss;
			oss << g;
			REQUIRE(oss.str() == "A (\n  C | 2\n)\nB (\n)\nC (\n)\n");
		}
		SECTION("return false") {
			REQUIRE(g.erase_edge("A", "B", 2) == false);
			std::ostringstream oss;
			oss << g;
			REQUIRE(oss.str() == "A (\n  B | 1\n  C | 2\n)\nB (\n)\nC (\n)\n");
		}
		SECTION("erase edge exception") {
			REQUIRE_THROWS_WITH(g.erase_edge("D", "E", 3),
			                    "Cannot call gdwg::graph<N, E>::erase_edge on src or dst if "
			                    "they don't exist in the graph");
		}
	}
}

TEST_CASE("Test for clear graph ") {
	gdwg::graph<std::string, int> g;
	g.insert_node("A");
	g.insert_node("B");
	g.insert_node("C");
	g.insert_edge("A", "B", 1);
	g.insert_edge("A", "C", 2);
	SECTION("graph should be empty after clear") {
		g.clear();
		REQUIRE(g.empty());
	}
}

TEST_CASE("empty test") {
	gdwg::graph<std::string, std::string> g;
	SECTION("node, connection should be empty as well") {
		REQUIRE(g.empty());
		auto ov = g.nodes();
		REQUIRE(ov.empty());
		REQUIRE_THROWS_WITH(g.connections("A"),
		                    "Cannot call gdwg::graph<N, E>::connections if src doesn't "
		                    "exist in the graph");
	}
}

// Accessors
TEST_CASE("Test is_node() ") {
	SECTION("A B C nodes graph not e") {
		gdwg::graph<std::string, std::string> g{"A", "B", "C"};
		REQUIRE(g.is_node("A") == true);
		REQUIRE(g.is_node("B") == true);
		REQUIRE(g.is_node("C") == true);
		REQUIRE(g.is_node("E") == false);
	}
}

TEST_CASE("Test is_connected() ") {
	SECTION("graph given (a, b, 1), (a, c, 2)") {
		gdwg::graph<std::string, int> g;
		g.insert_node("a");
		g.insert_node("b");
		g.insert_node("c");

		g.insert_edge("a", "b", 1);
		g.insert_edge("a", "c", 2);

		REQUIRE(g.is_connected("a", "b"));
		REQUIRE(g.is_connected("a", "c"));

		REQUIRE(!g.is_connected("b", "a"));
		REQUIRE(!g.is_connected("b", "c"));
	}
}

TEST_CASE("Test nodes() ") {
	SECTION("graph given (a, b, 1), (a, c, 2)") {
		gdwg::graph<std::string, std::string> g{"C", "B", "A"};
		std::vector<std::string> v{"A", "B", "C"};
		auto ov = g.nodes();
		REQUIRE(v.size() == ov.size());
		REQUIRE(v == ov);
	}
}

TEST_CASE("Test weights() ") {
	gdwg::graph<std::string, int> g;
	g.insert_node("a");
	g.insert_node("b");
	g.insert_node("c");

	g.insert_edge("a", "b", 3);
	g.insert_edge("a", "b", 1);
	g.insert_edge("a", "c", 2);
	SECTION("graph given (a, b, 1), (a, b, 3), (a, c, 2)") {
		auto v1 = g.weights("a", "b");
		std::vector<int> v2 = {1, 3};
		REQUIRE(v1 == v2);
	}
	SECTION("should return {} vector") {
		auto v1 = g.weights("b", "c");
		std::vector<int> v2 = {};
		REQUIRE(v1 == v2);
	}
	SECTION("weights exception") {
		REQUIRE_THROWS_WITH(g.weights("e", "z"),
		                    "Cannot call gdwg::graph<N, E>::weights if src or dst node "
		                    "don't exist in the graph");
	}
}

TEST_CASE("Test connections() ") {
	gdwg::graph<std::string, int> g;
	g.insert_node("a");
	g.insert_node("b");
	g.insert_node("c");

	g.insert_edge("a", "b", 1);
	g.insert_edge("a", "c", 2);
	SECTION("graph given (a, b, 1), (a, c, 2)") {
		auto v1 = g.connections("a");
		std::vector<std::string> v2{"b", "c"};
		REQUIRE(v1 == v2);
	}
	SECTION("should return {} vector") {
		auto v1 = g.connections("b");
		std::vector<std::string> v2 = {};
		REQUIRE(v1 == v2);
	}
	SECTION("connections exception") {
		REQUIRE_THROWS_WITH(g.connections("z"),
		                    "Cannot call gdwg::graph<N, E>::connections if src doesn't "
		                    "exist in the graph");
	}
}

// Iterator
TEST_CASE("Some Iterator test ") {
	gdwg::graph<std::string, int> g;
	g.insert_node("A");
	g.insert_node("B");
	g.insert_node("C");
	g.insert_edge("A", "B", 1);
	g.insert_edge("A", "C", 2);
	g.insert_edge("B", "A", 3);
	SECTION("find and erase") {
		auto it1 = g.find("A", "B", 1);
		REQUIRE(std::get<0>(*it1) == "A");
		REQUIRE(std::get<1>(*it1) == "B");
		REQUIRE(std::get<2>(*it1) == 1);
		auto it2 = g.erase_edge(it1);
		REQUIRE(std::get<0>(*it2) == "A");
		REQUIRE(std::get<1>(*it2) == "C");
		REQUIRE(std::get<2>(*it2) == 2);
	}
}

// Compairsons
TEST_CASE("Test == checking two graph is same or not") {
	gdwg::graph<std::string, int> k;
	gdwg::graph<std::string, int> l;
	gdwg::graph<std::string, int> m;
	gdwg::graph<std::string, int> n;
	k.insert_node("A");
	k.insert_node("B");
	k.insert_node("C");
	k.insert_edge("A", "B", 1);
	k.insert_edge("B", "C", 2);
	k.insert_edge("C", "A", 3);

	l.insert_node("A");
	l.insert_node("B");
	l.insert_node("C");
	l.insert_edge("A", "B", 1);
	l.insert_edge("B", "C", 2);
	l.insert_edge("C", "A", 3);

	m.insert_node("A");
	m.insert_node("B");
	m.insert_node("C");
	m.insert_edge("B", "A", 1);
	m.insert_edge("B", "C", 2);
	m.insert_edge("C", "A", 3);

	n.insert_node("A");
	n.insert_node("B");
	n.insert_edge("A", "B", 1);

	SECTION("same") {
		REQUIRE(k == l);
	}
	SECTION("not same") {
		REQUIRE(!(k == m));
	}
	SECTION("not same 2") {
		REQUIRE(!(k == n));
	}
}

TEST_CASE("Some General test") {
	SECTION("Modifiers test") {
		auto g = gdwg::graph<std::string, int>{};
		REQUIRE(g.empty());
		g.insert_node("A");
		g.insert_node("B");
		g.insert_node("C");
		g.insert_node("D");
		REQUIRE(!g.empty());
		REQUIRE(g.is_node("A"));
		REQUIRE(g.is_node("B"));
		REQUIRE(g.is_node("C"));
		REQUIRE(!g.insert_node("A"));
		REQUIRE(!g.insert_node("B"));
		g.insert_edge("A", "B", 5);
		g.insert_edge("A", "C", 7);
		g.insert_edge("A", "B", 10);
		g.insert_edge("B", "A", 1);
		g.insert_edge("B", "B", 3);
		g.insert_edge("B", "C", 5);
		REQUIRE(g.is_connected("A", "B"));
		REQUIRE(g.is_connected("B", "B"));
		auto v1 = g.nodes();
		auto expected_v1 = std::vector<std::string>{"A", "B", "C", "D"};
		REQUIRE(v1 == expected_v1);
		auto expected_v2 = std::vector<int>{5, 10};
		auto v2 = g.weights("A", "B");
		REQUIRE(v2 == expected_v2);
		auto expected_v3 = std::vector<std::string>{"A", "B", "C"};
		auto v3 = g.connections("B");
		REQUIRE(v3 == expected_v3);
		auto expected_v4 = std::vector<std::string>{"A", "B"};
		g.erase_edge("B", "C", 5);
		auto v4 = g.connections("B");
		REQUIRE(v4 == expected_v4);
		REQUIRE(!g.is_connected("B", "C"));
		g.insert_edge("B", "D", 7);
		g.replace_node("D", "E");
		REQUIRE(g.is_connected("B", "E"));
		g.erase_node("E");
	}
}

TEST_CASE("BakaTesu ") {
	gdwg::graph<std::string, int> g;
	g.insert_node("A");
	g.insert_node("B");
	g.insert_node("C");
	g.insert_node("D");
	g.insert_edge("A", "B", 1);
	g.insert_edge("A", "C", 2);
	g.insert_edge("A", "D", 3);
	g.insert_edge("B", "A", 3);
	g.insert_edge("B", "A", 5);
	g.insert_edge("B", "A", 7);
	g.insert_edge("D", "A", 7);
	SECTION("A Graph 'g' is constructed using three nodes {A,B,C} and 2 edges "
	        "from A->B and A->C") {
		auto itr = g.begin();
		// itr++;
		// itr++;
		// itr++;
		// itr++;
		// auto [from, to, weight] = *itr;
		while (itr != g.end()) {
			auto [from, to, weight] = *itr;
			std::cout << from << " " << to << " " << weight << "\n";
			itr++;
		}
		// std::cout << from << " " << to << " " << weight << "\n";
	}
}