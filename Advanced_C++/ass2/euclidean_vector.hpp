#ifndef COMP6771_EUCLIDEAN_VECTOR_HPP
#define COMP6771_EUCLIDEAN_VECTOR_HPP

#include "gsl-lite/gsl-lite.hpp"
#include <cmath>
#include <compare>
#include <functional>
#include <initializer_list>
#include <iostream>
#include <list>
#include <memory>
#include <ostream>
#include <range/v3/algorithm.hpp>
#include <range/v3/iterator.hpp>
#include <range/v3/view.hpp>
#include <span>
#include <stdexcept>
#include <string>
#include <string_view>
#include <type_traits>
#include <vector>

// z5186797 Yuta Sato
namespace comp6771 {
	using gsl_lite::narrow_cast;
	// class euclidean_vector_error : public std::runtime_error {
	// public:
	// 	explicit euclidean_vector_error(std::string const& what) noexcept
	// 	: std::runtime_error(what) {}
	// };
	class euclidean_vector_error : public std::runtime_error {
	public:
		explicit euclidean_vector_error(std::string const& what) noexcept
		: std::runtime_error(what) {}
	};

	class euclidean_vector {
	public:
		// Constructors---------------------------------------------------------------
		// Constructor (int, double)
		euclidean_vector(int size, double magnitude)
		// if just simple constrcutor use size_{size} but complivated wirte inside {}
		: size_{size} {
			// NOLINTNEXTLINE
			magnitudes_ = std::make_unique<double[]>(narrow_cast<unsigned long>(size));
			ranges::fill(magnitudes_.get(), magnitudes_.get() + size, magnitude);
		}

		// Default Constructor
		euclidean_vector()
		: euclidean_vector(1, 0.0) {}

		// Constructor (int)
		explicit euclidean_vector(int size)
		: size_{size} {
			// NOLINTNEXTLINE
			magnitudes_ = std::make_unique<double[]>(narrow_cast<unsigned long>(size));
			ranges::fill(magnitudes_.get(), magnitudes_.get() + size, 0.0);
		};

		// Constructor (std::vector code in cpp file)
		euclidean_vector(std::vector<double>::const_iterator begin,
		                 std::vector<double>::const_iterator end);

		// Constructor (std::list code in cpp file)
		euclidean_vector(std::initializer_list<double>);

		// copy constructor (code in cpp file)
		euclidean_vector(euclidean_vector const& v1);

		// move constructor (code in cpp file)
		euclidean_vector(euclidean_vector&& v1) noexcept;

		// destructer
		virtual ~euclidean_vector() = default;

		// operators--------------------------------------------------------
		auto operator[](int i) const {
			assert(i >= 0);
			return magnitudes_[narrow_cast<unsigned long>(i)];
		}

		auto operator[](int i) {
			assert(i >= 0);
			return magnitudes_[narrow_cast<unsigned long>(i)];
		}

		auto operator=(euclidean_vector const& v) -> euclidean_vector&;

		auto operator=(euclidean_vector&& v) noexcept -> euclidean_vector&;

		auto operator+() -> euclidean_vector;

		auto operator-() -> euclidean_vector;

		auto operator+=(euclidean_vector const& v) -> euclidean_vector&;

		auto operator-=(euclidean_vector const& v) -> euclidean_vector&;

		auto operator*=(double k) -> euclidean_vector&;

		auto operator/=(double k) -> euclidean_vector&;

		explicit operator std::vector<double>() const;

		explicit operator std::list<double>() const;

		// friends (should be inside class)--------------------------------------------------
		friend auto operator==(euclidean_vector const& v1, euclidean_vector const& v2) -> bool {
			if (v1.size_ != v2.size_) {
				return false;
			}
			for (auto i : ranges::views::iota(0, v1.dimensions())) {
				if (v1.magnitudes_[narrow_cast<unsigned long>(i)]
				    != v2.magnitudes_[narrow_cast<unsigned long>(i)]) {
					return false;
				}
			}
			return true;
		}

		friend auto operator!=(euclidean_vector const& v1, euclidean_vector const& v2) -> bool {
			if (v1.dimensions() != v2.dimensions()) {
				return true;
			}
			for (auto i : ranges::views::iota(0, v1.dimensions())) {
				if (v1.magnitudes_[narrow_cast<unsigned long>(i)]
				    != v2.magnitudes_[narrow_cast<unsigned long>(i)]) {
					return true;
				}
			}
			return false;
		}

		friend auto operator+(euclidean_vector const& v1, euclidean_vector const& v2)
		   -> euclidean_vector {
			if (v1.dimensions() != v2.dimensions()) {
				throw euclidean_vector_error("Dimensions of LHS(" + std::to_string(v1.dimensions())
				                             + ") and RHS(" + std::to_string(v2.dimensions())
				                             + ") do not match");
			}
			// auto v3 = v1;
			// v3 += v2;
			// return v3;
			// use += then write +
			auto v3 = v1;
			v3 += v2;
			return v3;
		}

		friend auto operator-(euclidean_vector const& v1, euclidean_vector const& v2)
		   -> euclidean_vector {
			if (v1.dimensions() != v2.dimensions()) {
				throw euclidean_vector_error("Dimensions of LHS(" + std::to_string(v1.dimensions())
				                             + ") and RHS(" + std::to_string(v2.dimensions())
				                             + ") do not match");
			}
			auto v3 = v1;
			v3 -= v2;
			return v3;
		}

		friend auto operator*(euclidean_vector const& v1, double k) -> euclidean_vector {
			auto v2 = v1;
			v2 *= k;
			return v2;
		}

		friend auto operator*(double k, euclidean_vector const& v1) -> euclidean_vector {
			auto v2 = v1;
			v2 *= k;
			return v2;
		}

		friend auto operator/(euclidean_vector const& v1, double k) -> euclidean_vector {
			if (k == 0) {
				throw euclidean_vector_error("Invalid vector division by 0");
			}
			auto v2 = v1;
			v2 /= k;
			return v2;
		}

		// Member Functions --------------------------------------------------
		[[nodiscard]] auto at(int x) const -> double {
			if (x < 0 or x >= size_) {
				throw euclidean_vector_error("Index " + std::to_string(x)
				                             + " is not valid for this euclidean_vector object");
			}
			return magnitudes_[narrow_cast<unsigned long>(x)];
		}

		[[nodiscard]] auto at(int x) -> double& {
			if (x < 0 or x >= size_) {
				throw euclidean_vector_error("Index " + std::to_string(x)
				                             + " is not valid for this euclidean_vector object");
			}
			return magnitudes_[narrow_cast<unsigned long>(x)];
		}

		[[nodiscard]] auto dimensions() const -> int {
			return this->size_;
		}

		friend auto operator<<(std::ostream& os, euclidean_vector const& v) -> std::ostream& {
			os << "[";
			for (auto i : ranges::views::iota(0, v.dimensions())) {
				os << v.magnitudes_[narrow_cast<unsigned long>(i)];
				if (i != v.size_ - 1) {
					os << " ";
				}
			}
			os << "]";
			return os;
		}

		template<typename T>
		struct is_real_number {
			static auto constexpr value = std::is_integral_v<T> || std::is_floating_point_v<T>;
		};

		template<typename T>
		auto is_element_number(T) -> bool {
			return static_cast<bool>(is_real_number<T>::value);
		}

		// [[nodiscard]] auto begin() const -> double {
		// 	return magnitudes_[0];
		// }

		// [[nodiscard]] auto end() const -> double {
		// 	return magnitudes_[narrow_cast<unsigned long>(size_ - 1)];
		// }

		template<typename T>
		auto median() const -> T {
			if (size_ % 2 == 0) {
				if constexpr (std::is_arithmetic_v<T>) {
					auto const& hi = std::next(magnitudes_.get(), size_ / 2);
					auto const& lo = std::prev(hi);
					return (*hi + *lo) / 2;
				}
			}
			return *std::next(magnitudes_.get(), size_ / 2);
		}

		virtual auto f() -> void {
			std::cout << "normal ev"
			          << "\n";
		}

		[[nodiscard]] auto size() const -> int {
			return size_;
		}

	private:
		// Using double[] like array like c since ass2 spec requires we use double[] instead of
		// std::vector NOLINTNEXTLINE
		std::unique_ptr<double[]> magnitudes_;
		// std::unique_ptr<double[]> magnitudes_;
		int size_;
	};

	class ac_euclidean_vector : public euclidean_vector {
	public:
		explicit ac_euclidean_vector(int x, int y)
		: euclidean_vector(x)
		, mega_size_{y} {}

		auto f() -> void override {
			std::cout << "AC ev"
			          << "\n";
		}
		auto sizeoo() -> int {
			return size() + mega_size_;
		}

		virtual ~ac_euclidean_vector() = default;

	private:
		int mega_size_;
	};

	class ac_ac_euclidean_vector : public ac_euclidean_vector {
	public:
		explicit ac_ac_euclidean_vector(int x, int y)
		: ac_euclidean_vector(x, y) {}

		auto f() -> void final {
			std::cout << "AC AC ev"
			          << "\n";
		}

		~ac_ac_euclidean_vector() override = default;

	private:
	};

	// Utility functions----------------------------------------------------------
	inline auto euclidean_norm(euclidean_vector const& v) -> double {
		if (v.dimensions() == 0) {
			throw euclidean_vector_error("euclidean_vector with no dimensions does not have a "
			                             "norm");
		}
		auto square = 0.0;
		for (auto i : ranges::views::iota(0, v.dimensions())) {
			square += pow(v.at(i), 2);
		}
		auto norm = std::sqrt(square);
		return norm;
	}

	inline auto unit(euclidean_vector const& v) -> euclidean_vector {
		if (v.dimensions() == 0) {
			throw euclidean_vector_error("euclidean_vector with no dimensions does not have a unit "
			                             "vector");
		}
		auto norm = euclidean_norm(v);
		if (norm == 0) {
			throw euclidean_vector_error("euclidean_vector with zero euclidean normal does not have a "
			                             "unit vector");
		}
		auto uv = v;
		uv /= norm;
		return uv;
	}

	inline auto dot(euclidean_vector& x, euclidean_vector& y) -> double {
		if (x.dimensions() != y.dimensions()) {
			throw euclidean_vector_error("Dimensions of LHS(" + std::to_string(x.dimensions())
			                             + ") and RHS(" + std::to_string(y.dimensions())
			                             + ") do not match");
		}
		auto dot_xy = 0.0;
		for (auto i : ranges::views::iota(0, x.dimensions())) {
			dot_xy += x.at(i) * y.at(i);
		}
		return dot_xy;
	}

} // namespace comp6771
#endif // COMP6771_EUCLIDEAN_VECTOR_HPP
