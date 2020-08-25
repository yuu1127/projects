// Copyright (c) Christopher Di Bella.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
#include "comp6771/euclidean_vector.hpp"
#include <cstddef>
#include <iterator>
#include <memory>
#include <span>

namespace comp6771 {

// Constrcutors
// std::vector to euclidean_vector
euclidean_vector::euclidean_vector(std::vector<double>::const_iterator begin,
                                   std::vector<double>::const_iterator end) {
  size_ = static_cast<int>(ranges::distance(begin, end));
  // NOLINTNEXTLINE
  magnitudes_ = std::make_unique<double[]>(static_cast<unsigned long>(size_));
  // std::copy(begin, end, magnitudes_);
  ranges::copy(begin, end, magnitudes_.get());
}

// std::list to euclidean_vector
euclidean_vector::euclidean_vector(std::initializer_list<double> v1) {
  size_ = static_cast<int>(ranges::distance(v1.begin(), v1.end()));
  // NOLINTNEXTLINE
  magnitudes_ = std::make_unique<double[]>(static_cast<unsigned long>(size_));
  ranges::copy(v1.begin(), v1.end(), magnitudes_.get());
}

// copy constrcutor
euclidean_vector::euclidean_vector(euclidean_vector const &v1) {
  // const auto& v2 = v1;
  size_ = v1.size_;
  // NOLINTNEXTLINE
  magnitudes_ = std::make_unique<double[]>(static_cast<unsigned long>(size_));
  ranges::copy(v1.magnitudes_.get(), v1.magnitudes_.get() + size_,
               magnitudes_.get());
}

// move constrcutor
euclidean_vector::euclidean_vector(euclidean_vector &&v1) noexcept {
  size_ = v1.size_;
  v1.size_ = 0;
  magnitudes_ = std::move(v1.magnitudes_);
}

// helper function to return size
auto euclidean_vector::get_size() const -> int const & { return size_; }

// Operators
// Copy Assignemnt
auto euclidean_vector::operator=(euclidean_vector const &v)
    -> euclidean_vector & {
  // assert(*this != v);
  if (this == &v) {
    return *this;
  }
  // size_ = v.size_;
  // // magnitudes_ = v.magnitudes_;
  // // NOLINTNEXTLINE
  // magnitudes_ = std::make_unique<double[]>(static_cast<unsigned
  // long>(size_)); for (int i = 0; i < this->get_size(); ++i) {
  // 	magnitudes_[static_cast<unsigned long>(i)] = v[i];
  // }
  // return *this;
  size_ = v.size_;
  // NOLINTNEXTLINE
  magnitudes_ = std::make_unique<double[]>(static_cast<unsigned long>(size_));
  ranges::copy(v.magnitudes_.get(), v.magnitudes_.get() + size_,
               magnitudes_.get());
  return *this;
}

// Move assignment
auto euclidean_vector::operator=(euclidean_vector &&v) noexcept
    -> euclidean_vector & {
  size_ = v.size_;
  v.size_ = 0;
  magnitudes_ = std::move(v.magnitudes_);
  return *this;
}

// Subscript for const
// auto euclidean_vector::operator[](int i) const {
// 	assert(i >= 0);
// 	return magnitudes_[static_cast<unsigned long>(i)];
// }

// Subscript
// auto euclidean_vector::operator[](int i) {
// 	assert(i >= 0);
// 	return magnitudes_[static_cast<unsigned long>(i)];
// }

// Unary plus
auto euclidean_vector::operator+() -> euclidean_vector {
  // size_ = 1 * size_;
  // magnitudes_ = 1.0 * magnitudes_;
  // auto sp = std::span<double>(magnitudes_.get(), static_cast<unsigned
  // long>(size_)); sp | ranges::views::transform([](double i) { return 1.0 * i;
  // }); for (int i = 0; i < size_; i++) { 	magnitudes_[static_cast<unsigned
  // long>(i)] *= 1.0;
  // }
  // magnitudes_ = span | ranges::views::filter([](double i) { return 1.0 * i;
  // });
  return comp6771::euclidean_vector(*this);
}

// Negation
// auto euclidean_vector::operator-() -> euclidean_vector {
// 	auto v = euclidean_vector(*this) * -1;
// }

// Compound Addition
auto euclidean_vector::operator+=(euclidean_vector const &v)
    -> euclidean_vector & {
  assert(size_ == v.size_);
  for (auto i : ranges::views::iota(0, size_)) {
    magnitudes_[static_cast<unsigned long>(i)] += v[i];
  }
  return *this;
}

// Compound Subtraction
auto euclidean_vector::operator-=(euclidean_vector const &v)
    -> euclidean_vector & {
  assert(size_ == v.size_);
  for (auto i : ranges::views::iota(0, size_)) {
    magnitudes_[static_cast<unsigned long>(i)] -= v[i];
  }
  return *this;
}

// Compound Multiplication
// auto euclidean_vector::operator*=(double i) -> euclidean_vector& {
// 	size_ = static_cast<int>(i) * size_;
// 	magnitudes_ = i * magnitudes_;
// 	return *this;
// }

// Compound Division
// auto euclidean_vector::operator/=(double i) -> euclidean_vector& {
// 	size_ = size_ / static_cast<int>(i);
// 	magnitudes_ = magnitudes_ / i;
// 	return *this;
// }

// euclidean_vector::operator std::vector<double>() const {
// 	auto dummy = static_cast<double>(size_);
// 	return std::vector(dummy, magnitude_);
// }

} // namespace comp6771
