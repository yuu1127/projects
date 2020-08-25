#include "comp6771/word_ladder.hpp"
#include <deque>
#include <string>
#include <vector>
#include <iostream>
#include <range/v3/range.hpp>
#include <range/v3/view.hpp>
#include <range/v3/numeric.hpp>
#include <absl/container/flat_hash_map.h>
#include <range/v3/algorithm.hpp>
//#include <gsl-lite/gsl-lite.hpp>

// Write your implementation here

// z5186797 Yuta Sato

// function for making relationship for word (catch adjacent words),I choose absl::flat_hash_set
// since it works really efficiently (store word using hash)
// and try to ranges (std20 libraries) as much as possible
auto get_word_relationshps(const std::string &word,
                                            const absl::flat_hash_set<std::string> &lexicon) -> std::vector<std::string>{
    // if find 1 word differnt in lexicon , add reltionships dics
    std::vector<std::string> n_words{};
    const std::string alpha = "abcdefghijklmnopqrstuvwxyz";
    for(std::string::size_type i = 0; i < ranges::size(word); ++i){
        auto original_char = word.at(i);

        // for(auto c='a'; c <= 'z'; c++){
        //     if(original_char == c){
        //         continue;
        //     }
        //     auto temp_word = word;
        //     temp_word.at(i) = c;
        //     if(lexicon.contains(temp_word)){
        //         n_words.push_back(temp_word);
        //     }
        // }

        for(const auto &c: alpha){
            if(original_char == c){
                continue;
            }
            auto temp_word = word;
            temp_word.at(i) = c;
            if(lexicon.contains(temp_word)){
                n_words.push_back(temp_word);
            }
        }
    }
    return n_words;
}

// word ladder algorithm is actually not so difficult
// each while loop try to get adjacent words for word placed front of queue
// then such as tree ,track words from root (BFS search)
// the point is we need to store every minimum path so cannot return instantly when find minimum path
// therefore use for loop with level to track every path of its level(num_in_level)
namespace word_ladder{
 auto generate(const std::string &from, const std::string &to, const absl::flat_hash_set<std::string> &lexicon)-> std::vector<std::vector<std::string>>{

    //std::vector<std::string> output;
    std::deque<std::vector<std::string>> ladders{{from}};
    auto seen = absl::flat_hash_set<std::string>();
    auto outputs = std::vector<std::vector<std::string>>{};
    //bool end = false;

    // start while
    while(!ladders.empty()){
      auto num_in_level = ranges::size(ladders);
      auto seen_this_level = absl::flat_hash_set<std::string>();

      for(auto i = std::deque<int>::size_type{0}; i < num_in_level; ++i){
         //std::string current_word = ladders.front();
         auto q_item = ladders.front();
         ladders.pop_front();
         //auto q_size = q_item.size();
         std::vector<std::string> next_level_ladders = get_word_relationshps(q_item.back(), lexicon);
        //  std::cout << "word relationship is: ";
        //  for(const auto & word : next_level_ladders){
        //     std::cout << word << ",";
        //  }
        //  std::cout << "\n";
         for(const auto &next_ladder: next_level_ladders){
            if(next_ladder == to){
                auto output = q_item;
                output.push_back(next_ladder);
                outputs.push_back(output);
            }
            else if(seen.contains(next_ladder)){
                continue;
            }
            seen_this_level.insert(next_ladder);
            //q_item.push_back(next_ladder);
            auto output1 = q_item;
            //output1.insert(output1.end(),next_ladder);
            output1.push_back(next_ladder);
            ladders.push_back(output1);
         }
      }
      if(!outputs.empty()){
        ranges::sort(outputs);
        return outputs;
      }
      seen.insert(ranges::begin(seen_this_level), ranges::end(seen_this_level));
    }
 if(!outputs.empty()){
   ranges::sort(outputs);
   }
 // std::cout << "exit !!!" << "\n";
 return outputs;
 }
} // namespace word_ladder