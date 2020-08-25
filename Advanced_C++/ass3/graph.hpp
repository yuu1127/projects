#ifndef GDWG_GRAPH_HPP
#define GDWG_GRAPH_HPP

#include <absl/container/flat_hash_map.h>
#include <concepts/concepts.hpp>
#include <exception>
#include <initializer_list>
#include <iostream>
#include <memory>
#include <ostream>
#include <range/v3/algorithm/for_each.hpp>
#include <range/v3/iterator.hpp>
#include <range/v3/utility.hpp>
#include <regex>
#include <stdexcept>
#include <utility>
#include <vector>

namespace gdwg {
	template<concepts::regular N, concepts::regular E>
	requires concepts::totally_ordered<N> //
	   and concepts::totally_ordered<E> //
	   class graph {
	public:
		struct value_type {
			N from;
			N to;
			E weight;
		};

		struct node;
		struct edge;
		struct node_comp;
		struct edge_comp;

		// custom iterator
		// class iterator;
		class iterator {
		public:
			using value_type = ranges::common_tuple<N, N, E>;
			using difference_type = std::ptrdiff_t;
			using iterator_category = std::bidirectional_iterator_tag;
			using pointer = ranges::common_tuple<N, N, E>*;
			using reference = ranges::common_tuple<const N&, const N&, const E&>;

			// auto operator*() const -> reference;
			using outer_it = typename std::map<std::shared_ptr<node>,
			                                   std::set<std::shared_ptr<edge>, edge_comp>,
			                                   node_comp>::const_iterator;
			using inner_it = typename std::set<std::shared_ptr<edge>, edge_comp>::const_iterator;

			// Iterator constructor
			iterator() = default;

			// iterator operator
			// Iterator source
			auto operator*() const -> reference {
				using result_type = ranges::common_tuple<const N&, const N&, const E&>;
				return result_type(outer_->first->getval(),
				                   // inner is set pointer, *inner is edge pointer
				                   (*inner_)->get_dst_val(),
				                   (*inner_)->get_wegiht());
			}

			auto operator->() const -> pointer {
				return &(operator*());
			}

			// Iterator traversal
			// increment
			auto operator++() -> iterator& {
				if (inner_ != outer_->second.cend()) {
					do {
						++inner_;
						if (inner_ == outer_->second.cend()) {
							break;
						}
					} while ((*inner_)->get_dst_val() == outer_->first->getval());

					if (inner_ != outer_->second.cend()) {
						return *this;
					}
				}

				if (inner_ == outer_->second.cend()) {
					++outer_;
					if (outer_ != out_sentinel) {
						inner_ = outer_->second.cbegin();
					}

					while (outer_ != out_sentinel and (*inner_)->get_dst_val() == outer_->first->getval())
					{
						++inner_;
						if (inner_ == outer_->second.cend()) {
							++outer_;
							if (outer_ == out_sentinel) {
								break;
							}
							inner_ = outer_->second.cbegin();
						}
					}

					if (outer_ != out_sentinel and inner_ != outer_->second.cend()) {
						return *this;
					}
				}

				// if(outer == out_sentinel) inner_= ?
				inner_ = outer_ == out_sentinel ? inner_it() : outer_->second.cbegin();
				return *this;

				// if (inner_ != outer_->second.cend()) {
				// 	++inner_;
				// 	if (inner_ != outer_->second.cend()) {
				// 		return *this;
				// 	}
				// }
				// ++outer_;
				// inner_ = outer_ == out_sentinel ? inner_it() : outer_->second.cbegin();
				// return *this;
			}

			auto operator++(int) -> iterator {
				auto temp = *this;
				++*this;
				return temp;
			}

			auto operator--() -> iterator& {
				// maybe incase ?? noneed this
				if (inner_ == inner_it()) {
					outer_ = ranges::prev(out_sentinel);
					inner_ = ranges::prev(outer_->second.end());
					return *this;
				}

				if (inner_ != outer_.begin()) {
					--inner_;
					return *this;
				}

				--outer_;
				inner_ = ranges::prev(outer_->second.end());
				return *this;
			}

			auto operator--(int) -> iterator {
				auto temp = *this;
				--*this;
				return *temp;
			}

			// Iterator comparison
			friend auto operator==(iterator const& itr1, iterator const& itr2) -> bool {
				return itr1.outer_ == itr2.outer_
				       and (itr1.outer_ == itr2.out_sentinel || itr1.inner_ == itr2.inner_);
			}

			// iterator function such as find begin

		private:
			typename std::map<std::shared_ptr<node>,
			                  std::set<std::shared_ptr<edge>, edge_comp>,
			                  node_comp>::const_iterator outer_;
			const typename std::map<std::shared_ptr<node>,
			                        std::set<std::shared_ptr<edge>, edge_comp>,
			                        node_comp>::const_iterator out_sentinel;
			typename std::set<std::shared_ptr<edge>, edge_comp>::const_iterator inner_;
			const typename std::set<std::shared_ptr<edge>, edge_comp>::const_iterator in_sentinel;

			friend class graph<N, E>;

			// constrcutor
			explicit iterator(const decltype(outer_)& outer,
			                  const decltype(out_sentinel)& outsentinel,
			                  const decltype(inner_)& inner,
			                  const decltype(in_sentinel)& insentinel)
			: outer_{outer}
			, out_sentinel{outsentinel}
			, inner_{inner}
			, in_sentinel{insentinel} {}
		};

		[[nodiscard]] auto begin() const -> iterator {
			return iterator(graph_.cbegin(), graph_.cend(), (graph_.cbegin())->second.cbegin(), {});
		}

		[[nodiscard]] auto end() const -> iterator {
			return iterator(graph_.cend(), graph_.cend(), (--graph_.cend())->second.cend(), {});
		}

		// Constructors---------------------------------------------------------------
		// Effects: Value initialises all members. Throws: Nothing.
		graph<N, E>() = default;

		// 2.2.3
		// Effects: Equivalent to: graph(il.begin(), il.end());
		graph(std::initializer_list<N> il) {
			for (const auto& n : il) {
				insert_node(n);
			}
		}

		// 2.2.4
		// Effects: Initialises the graph’s node collection with the range [first, last).
		template<ranges::forward_iterator I, ranges::sentinel_for<I> S>
		requires ranges::indirectly_copyable<I, N*> graph(I first, S last) {
			for (auto it = first; it != last; ++it) {
				this->insert_node(*it);
			}
		}

		// 2.2.5
		// Effects: Initialises the graph’s node and edge collections with the range [first, last).
		template<ranges::forward_iterator I, ranges::sentinel_for<I> S>
		requires ranges::indirectly_copyable<I, value_type*> graph(I first, S last) {
			for (auto it = first; it != last; ++it) {
				auto [from, to, weight] = *it;
				if (!this->is_node(from)) {
					this->insert_node(from);
				}
				if (!this->is_node(to)) {
					this->insert_node(to);
				}
				this->insert_edge(from, to, weight);
			}
		}

		// 2.2.6
		// move constructor
		graph(graph&& other) noexcept {
			this->graph_ = std::move(other.graph_);
		}

		// 2.2.7
		// Effects: All existing nodes and edges are either move-assigned to, or are destroyed.
		auto operator=(graph&& other) noexcept -> graph& {
			this->graph_ = std::move(other.graph_);
			return *this;
		}

		// 2.2.10 Postconditions: *this == other is true.
		graph(graph const& other) {
			graph_ = {};
			for (const auto& n : other.graph_) {
				this->insert_node(n.first->getval());
			}

			for (const auto& node : other.graph_) {
				const auto& values = node.second;
				for (const auto& e : values) {
					this->insert_edge(e->get_src_val(), e->get_dst_val(), e->get_wegiht());
				}
			}
		}

		// 2.2.11
		// copy assignment All iterators pointing to elements owned by *this prior to this operator’s
		// invocation are invalidated.
		auto operator=(graph const& other) -> graph& {
			if (this == &other) {
				return *this;
			}
			for (const auto& n : other.graph_) {
				this->insert_node(n.first->getval());
			}
			for (const auto& n : other.graph_) {
				for (const auto& e : other.graph_[n]) {
					this->insert_edge(e->get_src_val(), e->get_dst_val(), e->get_wegiht());
				}
			}
			return *this;
		}

		// 2.7 Extractor Effects: Behaves as a formatted output function of os.
		friend auto operator<<(std::ostream& os, graph const& g) -> std::ostream& {
			for (const auto& node : g.graph_) {
				os << node.first->getval() << " (\n";
				const auto& values = node.second;
				for (const auto& e : values) {
					if (e->get_src_val() == node.first->getval()) {
						os << "  " << e->get_dst_val() << " | " << e->get_wegiht() << "\n";
					}
				}
				os << ")\n";
			}
			return os;
		}

		// Your member functions go here

		// 2.3.1 insert node Effects: Adds a new node with value value to the graph if, and only if,
		// there is no node equivalent to value already stored.
		auto insert_node(N const& value) -> bool {
			if (this->is_node(value)) {
				return false;
			}
			auto new_node = std::make_shared<node>(node{value});
			auto tmp_edge = std::set<std::shared_ptr<edge>, edge_comp>{};
			graph_.emplace(new_node, tmp_edge);
			return true;
		}

		// 2.3.4 insert edge Effects: Adds a new edge representing src → dst with weight weight, if,
		// and only if, there is no edge equivalent to value_type{src, dst, weight} already stored.
		auto insert_edge(N const& src, N const& dst, E const& w) -> bool {
			if (!this->is_node(src) or !this->is_node(dst)) {
				throw ::std::runtime_error("Cannot call gdwg::graph<N, E>::insert_edge when either src "
				                           "or dst node does not exist");
			}
			const auto& src_p = find_npointer(src);
			const auto& dst_p = find_npointer(dst);
			auto new_edge = std::make_shared<edge>(edge{src_p, dst_p, w});
			auto found = graph_[src_p].find(new_edge);
			if (found != graph_[src_p].end()) {
				return false;
			}
			// outgoing edge
			graph_[src_p].insert(new_edge);
			// ingoing edge
			graph_[dst_p].insert(new_edge);
			return true;
		}

		// 2.3.8 replace node Effects: Replaces the original data, old_data, stored at this particular
		// node by the replacement data, new_data. Does nothing if new_data already exists as a node.
		auto replace_node(N const& old_data, N const& new_data) -> bool {
			if (!this->is_node(old_data)) {
				throw ::std::runtime_error("Cannot call gdwg::graph<N, E>::replace_node on a node"
				                           "that doesn't exist");
			}
			const auto& old_p = find_npointer(old_data);
			if (!this->is_node(new_data)) {
				auto np = graph_.extract(old_p);
				np.key()->setval(new_data);
				graph_.insert(std::move(np));
				return true;
			}
			return false;
		}

		// 2.3.9 merge replace node Effects: The node equivalent to old_data in the graph are replaced
		// with instances of new_data. After completing, every incoming and outgoing edge of old_data
		// becomes an incoming/ougoing edge of new_data, except that duplicate edges shall be removed.
		auto merge_replace_node(N const& old_data, N const& new_data) -> void {
			if (!this->is_node(old_data) or !this->is_node(new_data)) {
				throw ::std::runtime_error("Cannot call gdwg::graph<N, E>::merge_replace_node on old "
				                           "or new data if they don't exist in the graph");
			}
			// merge is just replace every edge value and delete edge for old node
			const auto& src_p = find_npointer(old_data);
			auto out_values = graph_[src_p];
			for (const auto& e : out_values) {
				auto n_src = e->get_src_val();
				auto n_dst = e->get_dst_val();
				// outgoing
				if (n_dst != old_data) {
					insert_edge(new_data, n_dst, e->get_wegiht());
				}
				else if (n_src != old_data) {
					insert_edge(n_src, new_data, e->get_wegiht());
				}
			}
			erase_node(old_data);
		}

		// 2.3.16 erase node Effects: Erases all nodes equivalent to value, including all incoming and
		// outgoing edges.
		auto erase_node(N const& value) -> bool {
			if (!is_node(value)) {
				return false;
			}
			const auto& src_p = find_npointer(value);
			// first erase ingoing edge
			auto out_values = graph_[src_p];
			for (const auto& e : out_values) {
				// remove outgoing
				erase_edge(value, e->get_dst_val(), e->get_wegiht());
				// remove ingoing
				erase_edge(e->get_src_val(), value, e->get_wegiht());
			}
			graph_[src_p].clear();
			graph_.erase(src_p);
			return true;
		}

		// 2.3.20 erase edge Effects: Erases an edge representing src → dst with weight weight.
		auto erase_edge(N const& src, N const& dst, E const& weight) -> bool {
			if (!this->is_node(src) or !this->is_node(dst)) {
				throw ::std::runtime_error("Cannot call gdwg::graph<N, E>::erase_edge on src or dst if "
				                           "they don't exist in the graph");
			}
			const auto& src_p = find_npointer(src);
			const auto& dst_p = find_npointer(dst);
			auto out_values = graph_[src_p];
			auto in_values = graph_[dst_p];
			for (const auto& e : out_values) {
				if (e.get()->get_dst_val() == dst and e.get()->get_wegiht() == weight) {
					// erase just edge
					graph_[src_p].erase(e);
					break;
				}
			}

			for (const auto& e : in_values) {
				if (e.get()->get_src_val() == src and e.get()->get_wegiht() == weight) {
					// erase just edge
					graph_[dst_p].erase(e);
					return true;
				}
			}
			return false;
		}

		auto erase_edge(iterator i) -> iterator {
			if (i == this->end()) {
				return this->end();
			}
			const auto& [from, to, weight] = *i;
			auto found = find(from, to, weight);
			if (found != this->end()) {
				++found;
				erase_edge(from, to, weight);

				const auto& [from, to, weight] = *found;
				return find(from, to, weight);
			}
			return this->end();
		}

		auto erase_edge(iterator i, iterator s) -> iterator {
			if (i == this->end() or s == this->end()) {
				return this->end();
			}
			const auto& [from, to, weight] = *s;
			auto found = find(from, to, weight);
			if (found != this->end() and found != this->begin()) {
				--found;
				auto it = i;
				for (it = i; it != s; ++it) {
					erase_edge(it);
				}
				const auto& [from, to, weight] = *found;
				return find(from, to, weight);
			}
			return this->end();
		}

		// 2.3.33 clear graph Effects: Erases all nodes from the graph.
		auto clear() noexcept -> void {
			graph_.clear();
		}

		// accesoors here

		// 2.3.1 is_node Returns: true if a node equivalent to value exists in the graph, and false
		// otherwise.
		[[nodiscard]] auto is_node(N const& value) -> bool {
			auto found = graph_.find(value);
			return found != graph_.end();
		}

		// 2.4.3 empty Returns: true if there are no nodes in the graph, and false otherwise.
		[[nodiscard]] auto empty() -> bool {
			return static_cast<bool>(graph_.empty());
		}

		// 2.4.4 is_connected Returns: true if an edge src → dst exists in the graph, and false
		// otherwise.
		[[nodiscard]] auto is_connected(N const& src, N const& dst) -> bool {
			if (!this->is_node(src) or !this->is_node(dst)) {
				throw ::std::runtime_error("Cannot call gdwg::graph<N, E>::is_connected if src or dst "
				                           "node don't exist in the graph");
			}
			const auto& src_p = find_npointer(src);
			auto values = graph_[src_p];
			for (const auto& e : values) {
				if (e->get_dst_val() == dst) {
					return true;
				}
			}
			return false;
		}

		// 2.4.6 nodes Returns: A sequence of all stored nodes, sorted in ascending order.
		[[nodiscard]] auto nodes() -> std::vector<N> {
			std::vector<N> v;
			for (const auto& n : graph_) {
				v.push_back(n.first->getval());
			}
			// ranges::for_each(graph_, [&](const auto& n){
			// 	v.push_back(n.first->getval());
			// });
			std::sort(v.begin(), v.end());
			return v;
		}

		// 2.4.8 weights Returns: A sequence of weights from src to dst, sorted in ascending order.
		[[nodiscard]] auto weights(N const& src, N const& dst) -> std::vector<E> {
			if (!this->is_node(src) or !this->is_node(dst)) {
				throw ::std::runtime_error("Cannot call gdwg::graph<N, E>::weights if src or dst node "
				                           "don't exist in the graph");
			}
			std::vector<E> v;
			const auto& src_p = find_npointer(src);
			auto values = graph_[src_p];
			for (const auto& e : values) {
				if (e->get_dst_val() == dst) {
					v.push_back(e->get_wegiht());
				}
			}
			std::sort(v.begin(), v.end());
			return v;
		}

		// 2.4.11 find Returns: An iterator pointing to an edge equivalent to value_type{src, dst,
		// weight}, or end() if no such edge exists.
		[[nodiscard]] auto find(N const& src, N const& dst, E const& weight) -> iterator {
			if (!this->is_node(src) or !this->is_node(dst)) {
				return this->end();
			}
			for (auto it = this->begin(); it != this->end(); ++it) {
				auto [from, to, weight_] = *it;
				if (from == src and to == dst and weight_ == weight) {
					return it;
				}
			}
			return this->end();
		}

		// 2.4.13 connections Returns: A sequence of nodes (found from any immediate outgoing edge)
		// connected to src, sorted in ascending order, with respect to the connected nodes.
		[[nodiscard]] auto connections(N const& src) -> std::vector<N> {
			if (!this->is_node(src)) {
				throw ::std::runtime_error("Cannot call gdwg::graph<N, E>::connections if src doesn't "
				                           "exist in the graph");
			}
			std::vector<N> v;
			const auto& src_p = find_npointer(src);
			auto values = graph_[src_p];
			for (const auto& e : values) {
				if (e->get_src_val() == src) {
					v.push_back(e->get_dst_val());
				}
			}
			std::sort(v.begin(), v.end());
			return v;
		}

		// 2.6 Comparisons
		// Returns: true if *this and other contain exactly the same nodes and edges, and false
		// otherwise.
		[[nodiscard]] auto operator==(graph const& other) const -> bool {
			if (graph_.size() != other.graph_.size()) {
				return false;
			}
			auto itr1 = graph_.begin();
			auto itr2 = other.graph_.begin();
			auto end1 = graph_.end();

			while (itr1 != end1) {
				const auto& node_a = *itr1;
				const auto& node_b = *itr2;
				const auto& values_a = node_a.second;
				const auto& values_b = node_b.second;

				if (node_a.first->getval() != node_b.first->getval()) {
					return false;
				}

				if (values_a.size() != values_b.size()) {
					return false;
				}

				auto in_itr1 = values_a.begin();
				auto in_itr2 = values_b.begin();
				auto end2 = values_a.end();

				while (in_itr1 != end2) {
					const auto& edge_a = *in_itr1;
					const auto& edge_b = *in_itr2;
					auto flag1 = edge_a->get_src_val() != edge_b->get_src_val();
					auto flag2 = edge_b->get_dst_val() != edge_b->get_dst_val();
					auto flag3 = edge_a->get_wegiht() != edge_b->get_wegiht();

					if (flag1 or flag2 or flag3) {
						return false;
					}
					++in_itr1;
					++in_itr2;
				}
				++itr1;
				++itr2;
			}
			return true;
		}

		// my structure here
		// node comparator for node construct
		struct node_comp {
			using is_transparent = void;

			auto operator()(const std::shared_ptr<node>& lhs, const std::shared_ptr<node>& rhs) const
			   -> bool {
				return *lhs < *rhs;
			}
			auto operator()(const N& left, const std::shared_ptr<node>& rhs) const -> bool {
				return left < rhs->getval();
			}
			auto operator()(const std::shared_ptr<node>& lhs, const N& right) const -> bool {
				return lhs->getval() < right;
			}
		};

		// edge comparator for edge construct

		struct edge_comp {
			using is_transparent = void;

			auto operator()(const std::shared_ptr<edge>& lhs, const std::shared_ptr<edge>& rhs) const
			   -> bool {
				return *lhs < *rhs;
			}
			auto operator()(const E& left, const std::shared_ptr<edge>& rhs) const -> bool {
				return left < rhs->get_wegiht();
			}
			auto operator()(const std::shared_ptr<edge>& lhs, const E& right) const -> bool {
				return lhs->get_wegiht() < right;
			}
		};

		// struct node value is start node N val_
		struct node {
			node() = default;
			explicit node(const N& val)
			: val_{val} {}

			auto getval() -> const N& {
				return val_;
			}

			auto setval(const N& val) -> const N& {
				val_ = val;
				return val_;
			}

			auto operator*() -> N {
				return val_;
			};

			friend auto operator<(const node& node_a, const node& node_b) -> bool {
				return node_a.val_ < node_b.val_;
			}

			friend auto operator==(const node& node_a, const node& node_b) -> bool {
				return node_a.val_ == node_b.val_;
			}

			friend auto operator!=(const node& node_a, const node& node_b) -> bool {
				return node_a.val_ != node_b.val_;
			}

		private:
			N val_;
		};

		// struct edge value is start node N src_, destination node N dst_, weight E weight_
		// to store outgoing edge and ingoing edge I store start node as well in my structure

		struct edge {
			edge() = default;
			edge(std::shared_ptr<node> src, std::shared_ptr<node> dst, const E& w) {
				src_ = std::weak_ptr<node>(src);
				dst_ = std::weak_ptr<node>(dst);
				weight_ = w;
			}

			auto get_dst_p() -> std::weak_ptr<node> {
				return dst_;
			}

			auto get_src_val() -> const N& {
				// to take value from weakpointer need lock
				return src_.lock()->getval();
			}

			auto get_dst_val() -> const N& {
				return dst_.lock()->getval();
			}

			auto get_wegiht() -> const E& {
				return weight_;
			}

			auto operator*() -> E {
				return weight_;
			};

			friend auto operator<(const edge& a, const edge& b) -> bool {
				auto flag1 = a.src_.lock()->getval() == b.src_.lock()->getval();
				auto flag2 = a.dst_.lock()->getval() == b.dst_.lock()->getval();
				if (flag1 && flag2) {
					return a.weight_ < b.weight_;
				}
				if (flag1) {
					return a.dst_.lock()->getval() < b.dst_.lock()->getval();
				}
				return a.src_.lock()->getval() < b.src_.lock()->getval();
			}

			friend auto operator==(const edge& node_a, const edge& node_b) -> bool {
				auto flag1 = node_a.src_.lock()->getval() == node_b.src_.lock()->getval();
				auto flag2 = node_a.dst_.lock()->getval() == node_b.dst_.lock()->getval();
				auto flag3 = node_a.get_wegiht() == node_b.get_wegiht();

				return flag1 and flag2 and flag3;
			}

			friend auto operator!=(const edge& node_a, const edge& node_b) -> bool {
				auto flag1 = node_a.src_.lock()->getval() != node_b.src_.lock()->getval();
				auto flag2 = node_a.dst_.lock()->getval() != node_b.dst_.lock()->getval();
				auto flag3 = node_a.get_wegiht() != node_b.get_wegiht();

				return flag1 or flag2 or flag3;
			}

			// auto operator<(const edge& b) -> bool {
			// 	auto flag1 = src_.lock()->getval() == b.src_.lock()->getval();
			// 	auto flag2 = dst_.lock()->getval() == b.dst_.lock()->getval();
			// 	if (flag1 && flag2) {
			// 		return weight_ < b.weight_;
			// 	}
			// 	if (flag1) {
			// 		return dst_.lock()->getval() < b.dst_.lock()->getval();
			// 	}
			// 	return src_.lock()->getval() < b.src_.lock()->getval();
			// }

			// auto operator==(const edge& node_b) -> bool {
			// 	auto flag1 = src_.lock()->getval() == node_b.src_.lock()->getval();
			// 	auto flag2 = dst_.lock()->getval() == node_b.dst_.lock()->getval();
			// 	auto flag3 = weight_ == node_b.get_wegiht();

			// 	return flag1 and flag2 and flag3;
			// }

			// auto operator!=(const edge& node_b) -> bool {
			// 	auto flag1 = src_.lock()->getval() != node_b.src_.lock()->getval();
			// 	auto flag2 = dst_.lock()->getval() != node_b.dst_.lock()->getval();
			// 	auto flag3 = weight_ != node_b.get_wegiht();

			// 	return flag1 or flag2 or flag3;
			// }

		private:
			E weight_;
			std::weak_ptr<node> src_;
			std::weak_ptr<node> dst_;
		};

		// helper function to return pointer for node
		auto find_npointer(const N& val) const -> std::shared_ptr<node> {
			for (const auto& n : graph_) {
				if (n.first->getval() == val) {
					return n.first;
				}
			}
			return {};
		}

	private:
		// my graph structure map(key:shared pointer of node value:set(shared pointer of edge))
		std::map<std::shared_ptr<node>, std::set<std::shared_ptr<edge>, edge_comp>, node_comp> graph_;
	};
} // namespace gdwg

#endif // GDWG_GRAPH_HPP
