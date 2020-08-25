//
//  Copyright UNSW Sydney School of Computer Science and Engineering
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

// z5185797 Yuta Sato

// Test description
// I decide to categorize test case to 3 , since if some specific test fail,
// it is relatively easy to detect whcih part we need to work on and fix . (e.g. if size test fail, we can check range, length part to do debug.)
// For each test, I have used 5 type input output words(separeted by using section) to test various type of inputs
// such as from at -> it (shortest path) code -> data (3 shortest path) airplane -> tricycle (no path) and so on.
// Since we can assume start word and end word has same length, there are in lexicon, they are not same words,
// I didn't include these edge cases.

// 1.General accuracy test
// In this test, it implements general tests to check whether the outputs
// contain correct expected outputs or not.

// 2.Size Test
// In this test, it checks the size of output is same as expected size.

// 3.Sort Test
// In this test, it evaluates the output ladders is sorted or not.


#include "comp6771/word_ladder.hpp"
#include <string>
#include <vector>
#include "catch2/catch.hpp"
#include "comp6771/testing/range/contain.hpp"
#include "range/v3/algorithm/any_of.hpp"
#include "range/v3/algorithm/is_sorted.hpp"
#include "range/v3/range/primitives.hpp"
#include <iostream>

TEST_CASE("1:general accuracy test") {
	auto const english_lexicon = word_ladder::read_lexicon("./english.txt");
	std::cout << "general test start" << std::endl;

	SECTION("at -> it"){
		auto const ladders = word_ladder::generate("at", "it", english_lexicon);
		std::vector<std::vector<std::string>> expected_ladders{
        {"at","it"}
    };
		CHECK(ladders == expected_ladders);
	}

	SECTION("awake -> sleep"){
		auto const ladders = word_ladder::generate("awake", "sleep", english_lexicon);
		std::vector<std::vector<std::string>> expected_ladders{
        {"awake","aware","sware","share","sharn","shawn","shewn","sheen","sheep","sleep"},
        {"awake","aware","sware","share","shire","shirr","shier","sheer","sheep","sleep"}
    };
		CHECK(ladders == expected_ladders);
	}

	SECTION("code -> data"){
		auto const ladders = word_ladder::generate("code", "data", english_lexicon);

		std::vector<std::vector<std::string>> expected_ladders{
				{"code", "cade", "cate", "date", "data"},
				{"code", "cote", "cate", "date", "data"},
				{"code", "cote", "dote", "date", "data"}
    };

        // std::cout << "ladders are" << "\n";
		// for(const auto & ladder : ladders){
		// 	for(const auto & word : ladder){
		// 		std::cout << word << ",";
		// 	}
	    //      std::cout << "\n";
	    // }

		CHECK(ladders == expected_ladders);
	}

	SECTION("work -> play"){
		auto const ladders = word_ladder::generate("work", "play", english_lexicon);
		std::vector<std::vector<std::string>> expected_ladders{
        {"work", "fork", "form", "foam", "flam", "flay", "play"},
        {"work", "pork", "perk", "peak", "pean", "plan", "play"},
        {"work", "pork", "perk", "peak", "peat", "plat", "play"},
        {"work", "pork", "perk", "pert", "peat", "plat", "play"},
        {"work", "pork", "porn", "pirn", "pian", "plan", "play"},
        {"work", "pork", "port", "pert", "peat", "plat", "play"},
        {"work", "word", "wood", "pood", "plod", "ploy", "play"},
        {"work", "worm", "form", "foam", "flam", "flay", "play"},
        {"work", "worn", "porn", "pirn", "pian", "plan", "play"},
        {"work", "wort", "bort", "boat", "blat", "plat", "play"},
        {"work", "wort", "port", "pert", "peat", "plat", "play"},
        {"work", "wort", "wert", "pert", "peat", "plat", "play"}
        };
		CHECK(ladders == expected_ladders);
	}

	SECTION("airplane -> tricycle"){
		auto const ladders = word_ladder::generate("airplane", "tricycle", english_lexicon);
		std::vector<std::vector<std::string>> expected_ladders{
    };
		CHECK(ladders == expected_ladders);
	}

}


//  TEST2 no need to test every words pick 2 or 3
TEST_CASE("2:size test") {
	auto const english_lexicon = word_ladder::read_lexicon("./english.txt");
	std::cout << "size test start" << std::endl;

	SECTION("at -> it"){
		auto const ladders = word_ladder::generate("at", "it", english_lexicon);
		//CHECK(ranges::is_sorted(ladders));
		CHECK(ranges::size(ladders) == 1);
	}

	SECTION("awake -> sleep"){
		auto const ladders = word_ladder::generate("awake", "sleep", english_lexicon);
		CHECK(ranges::size(ladders) == 2);
	}

	SECTION("code -> data"){
		auto const ladders = word_ladder::generate("code", "data", english_lexicon);
		CHECK(ranges::size(ladders) == 3);
	}

	SECTION("work -> play"){
		auto const ladders = word_ladder::generate("work", "play", english_lexicon);
		CHECK(ranges::size(ladders) == 12);
	}

	SECTION("airplane -> tricycle"){
		auto const ladders = word_ladder::generate("airplane", "tricycle", english_lexicon);
		CHECK(ranges::size(ladders) == 0);
	}

}

TEST_CASE("3:sort test") {
	auto const english_lexicon = word_ladder::read_lexicon("./english.txt");
	std::cout << "sort test start" << std::endl;

	SECTION("at -> it"){
		auto const ladders = word_ladder::generate("at", "it", english_lexicon);
		CHECK(ranges::is_sorted(ladders));
	}

	SECTION("awake -> sleep"){
		auto const ladders = word_ladder::generate("awake", "sleep", english_lexicon);
		CHECK(ranges::is_sorted(ladders));
	}

	SECTION("code -> data"){
		auto const ladders = word_ladder::generate("code", "data", english_lexicon);
		CHECK(ranges::is_sorted(ladders));
	}

	SECTION("work -> play"){
		auto const ladders = word_ladder::generate("work", "play", english_lexicon);
		CHECK(ranges::is_sorted(ladders));
	}

	SECTION("airplane -> tricycle"){
		auto const ladders = word_ladder::generate("airplane", "tricycle", english_lexicon);
		CHECK(ranges::is_sorted(ladders));
	}

}

// TEST_CASE("4:edge test") {
// 	auto const english_lexicon = word_ladder::read_lexicon("./english.txt");
// 	std::cout << "general test start" << std::endl;
// 	auto const ladders = word_ladder::generate("at", "it", english_lexicon);
// 	//std::cout << "kunisiro" << std::endl;
// 	CHECK(ranges::size(ladders) == 1);
// 	CHECK(ranges::is_sorted(ladders));
//
// 	std::cout << "ladders are" << "\n";
// 	for(const auto & ladder : ladders){
// 		for(const auto & word : ladder){
// 			std::cout << word << ",";
// 		}
//          std::cout << "\n";
//     }
// }