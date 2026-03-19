#pragma once
/**
 * @file sdt_math.hpp
 * @brief Lightweight vector/matrix math — drop-in Eigen::Vector3d replacement.
 *        Pure C++20, no external dependencies.
 */

#include <cmath>
#include <numbers>

namespace sdt::math {

template<typename T>
struct Vec3 {
    T x_{}, y_{}, z_{};

    constexpr Vec3() = default;
    constexpr Vec3(T x, T y, T z) : x_(x), y_(y), z_(z) {}

    // Eigen-compatible accessors
    [[nodiscard]] constexpr T  x() const { return x_; }
    [[nodiscard]] constexpr T  y() const { return y_; }
    [[nodiscard]] constexpr T  z() const { return z_; }
    [[nodiscard]] constexpr T& x()       { return x_; }
    [[nodiscard]] constexpr T& y()       { return y_; }
    [[nodiscard]] constexpr T& z()       { return z_; }

    // Subscript operator (Eigen-compatible)
    [[nodiscard]] constexpr T  operator[](int i) const { return i == 0 ? x_ : (i == 1 ? y_ : z_); }
    [[nodiscard]] constexpr T& operator[](int i) { return i == 0 ? x_ : (i == 1 ? y_ : z_); }
    [[nodiscard]] constexpr T  operator()(int i) const { return (*this)[i]; }
    [[nodiscard]] constexpr T& operator()(int i) { return (*this)[i]; }

    // Factory
    [[nodiscard]] static constexpr Vec3 Zero() { return {T(0), T(0), T(0)}; }

    // Arithmetic
    constexpr Vec3 operator+(const Vec3& o) const { return {x_ + o.x_, y_ + o.y_, z_ + o.z_}; }
    constexpr Vec3 operator-(const Vec3& o) const { return {x_ - o.x_, y_ - o.y_, z_ - o.z_}; }
    constexpr Vec3 operator*(T s)           const { return {x_ * s,    y_ * s,    z_ * s};    }
    constexpr Vec3 operator/(T s)           const { return {x_ / s,    y_ / s,    z_ / s};    }
    constexpr Vec3 operator-()              const { return {-x_, -y_, -z_}; }

    constexpr Vec3& operator+=(const Vec3& o) { x_ += o.x_; y_ += o.y_; z_ += o.z_; return *this; }
    constexpr Vec3& operator-=(const Vec3& o) { x_ -= o.x_; y_ -= o.y_; z_ -= o.z_; return *this; }
    constexpr Vec3& operator*=(T s)           { x_ *= s;    y_ *= s;    z_ *= s;    return *this; }
    constexpr Vec3& operator/=(T s)           { x_ /= s;    y_ /= s;    z_ /= s;    return *this; }

    // Dot / Cross
    [[nodiscard]] constexpr T dot(const Vec3& o)   const { return x_*o.x_ + y_*o.y_ + z_*o.z_; }
    [[nodiscard]] constexpr Vec3 cross(const Vec3& o) const {
        return {y_*o.z_ - z_*o.y_,
                z_*o.x_ - x_*o.z_,
                x_*o.y_ - y_*o.x_};
    }

    // Norms
    [[nodiscard]] constexpr T squaredNorm() const { return dot(*this); }
    [[nodiscard]] T norm()           const { return std::sqrt(squaredNorm()); }
    [[nodiscard]] Vec3 normalized()  const { T n = norm(); return n > T(0) ? *this / n : Zero(); }

    // Mutating
    void setZero() { x_ = y_ = z_ = T(0); }
};

// scalar * Vec3
template<typename T>
constexpr Vec3<T> operator*(T s, const Vec3<T>& v) { return v * s; }

// Common aliases (match Eigen naming)
using Vec3d = Vec3<double>;
using Vec3f = Vec3<float>;

// ============================================================
// Minimal 4×4 matrix (for camera/view transforms only)
// ============================================================
template<typename T>
struct Mat4 {
    T data[16]{};  // column-major

    constexpr Mat4() = default;

    [[nodiscard]] static constexpr Mat4 Identity() {
        Mat4 m;
        m(0,0) = m(1,1) = m(2,2) = m(3,3) = T(1);
        return m;
    }

    [[nodiscard]] static constexpr Mat4 Zero_() {
        return Mat4{};
    }

    // (row, col) access — column-major storage
    [[nodiscard]] constexpr T  operator()(int r, int c) const { return data[c * 4 + r]; }
    [[nodiscard]] constexpr T& operator()(int r, int c)       { return data[c * 4 + r]; }
};

using Mat4d = Mat4<double>;
using Mat4f = Mat4<float>;

} // namespace sdt::math
