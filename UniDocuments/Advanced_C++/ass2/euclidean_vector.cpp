// Copyright (c) Christopher Di Bella.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
#include "comp6771/euclidean_vector.hpp"
#include <cstddef>
#include <iterator>
#include <memory>
#include <span>
#include <vector>

// z5186797 Yuta Sato
namespace comp6771 {
	using gsl_lite::narrow_cast;

	// Constrcutors---------------------------------------------------------------
	// Constructor (std::vector)
	euclidean_vector::euclidean_vector(std::vector<double>::const_iterator begin,
	                                   std::vector<double>::const_iterator end) {
		size_ = narrow_cast<int>(ranges::distance(begin, end));
		// NOLINTNEXTLINE
		magnitudes_ = std::make_unique<double[]>(narrow_cast<unsigned long>(size_));
		ranges::copy(begin, end, magnitudes_.get());
	}

	// Constructor (std::list)
	euclidean_vector::euclidean_vector(std::initializer_list<double> v1) {
		size_ = narrow_cast<int>(ranges::distance(v1.begin(), v1.end()));
		// NOLINTNEXTLINE
		magnitudes_ = std::make_unique<double[]>(narrow_cast<unsigned long>(size_));
		ranges::copy(v1.begin(), v1.end(), magnitudes_.get());
	}

	// copy constrcutor
	euclidean_vector::euclidean_vector(euclidean_vector const& v1) {
		size_ = v1.size_;
		// NOLINTNEXTLINE
		magnitudes_ = std::make_unique<double[]>(narrow_cast<unsigned long>(size_));
		ranges::copy(v1.magnitudes_.get(), v1.magnitudes_.get() + size_, magnitudes_.get());
	}

	// move constrcutor
	euclidean_vector::euclidean_vector(euclidean_vector&& v1) noexcept {
		size_ = v1.size_;
		v1.size_ = 0;
		magnitudes_ = std::move(v1.magnitudes_);
	}

	// Operators---------------------------------------------------------------------
	// Copy Assignemnt
	auto euclidean_vector::operator=(euclidean_vector const& v) -> euclidean_vector& {
		if (this == &v) {
			return *this;
		}
		size_ = v.size_;
		// NOLINTNEXTLINE
		magnitudes_ = std::make_unique<double[]>(narrow_cast<unsigned long>(size_));
		ranges::copy(v.magnitudes_.get(), v.magnitudes_.get() + size_, magnitudes_.get());
		return *this;
	}

	// Move assignment
	auto euclidean_vector::operator=(euclidean_vector&& v) noexcept -> euclidean_vector& {
		size_ = v.size_;
		v.size_ = 0;
		magnitudes_ = std::move(v.magnitudes_);
		return *this;
	}

	// Unary plus
	auto euclidean_vector::operator+() -> euclidean_vector {
		return *this;
	}

	// Negation
	auto euclidean_vector::operator-() -> euclidean_vector {
		auto v = (*this) * -1;
		return v;
	}

	// Compound Addition
	auto euclidean_vector::operator+=(euclidean_vector const& v) -> euclidean_vector& {
		if (this->dimensions() != v.dimensions()) {
			throw euclidean_vector_error("Dimensions of LHS(" + std::to_string(this->dimensions())
			                             + ") and RHS(" + std::to_string(v.dimensions())
			                             + ") do not match");
		}
		for (auto i : ranges::views::iota(0, size_)) {
			magnitudes_[narrow_cast<unsigned long>(i)] += v[i];
		}
		return *this;
	}

	// Compound Subtraction
	auto euclidean_vector::operator-=(euclidean_vector const& v) -> euclidean_vector& {
		if (this->dimensions() != v.dimensions()) {
			throw euclidean_vector_error("Dimensions of LHS(" + std::to_string(this->dimensions())
			                             + ") and RHS(" + std::to_string(v.dimensions())
			                             + ") do not match");
		}
		for (auto i : ranges::views::iota(0, size_)) {
			magnitudes_[narrow_cast<unsigned long>(i)] -= v[i];
		}
		return *this;
	}

	// Compound Multiplication
	auto euclidean_vector::operator*=(double k) -> euclidean_vector& {
		for (auto i : ranges::views::iota(0, size_)) {
			magnitudes_[narrow_cast<unsigned long>(i)] *= k;
		}
		return *this;
	}

	// Compound Division
	auto euclidean_vector::operator/=(double k) -> euclidean_vector& {
		for (auto i : ranges::views::iota(0, size_)) {
			magnitudes_[narrow_cast<unsigned long>(i)] /= k;
		}
		return *this;
	}

	// Vector Type Conversion
	euclidean_vector::operator std::vector<double>() const {
		auto new_v = std::vector<double>{};
		for (auto i : ranges::views::iota(0, size_)) {
			new_v.push_back(magnitudes_[narrow_cast<unsigned long>(i)]);
		}
		return new_v;
	}

	// euclidean_vector::operator std::vector<double>() const {
	// 	auto new_v = std::vector<double>{}
	// }

	// List Type Conversion
	euclidean_vector::operator std::list<double>() const {
		auto new_v = std::list<double>{};
		for (auto i : ranges::views::iota(0, size_)) {
			new_v.push_back(magnitudes_[narrow_cast<unsigned long>(i)]);
		}
		return new_v;
	}

} // namespace comp6771
