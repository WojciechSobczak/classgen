#pragma once

#include <string>
#include <string_view>
#include <sstream>
#include <map>
#include <inttypes.h>
#include <concepts>
#include <set>

namespace classgen
{
    constexpr std::size_t fnv_1a_hash(const std::string_view text)
    {
        //Diffrent constants for 32 an 64 bit
        constexpr std::size_t fnv_prime = sizeof(size_t) == 4 ? 16777619u : 1099511628211u;
        constexpr std::size_t fnv_offset_basis = sizeof(size_t) == 4 ? 2166136261u : 14695981039346656037u;
        std::size_t hash = fnv_offset_basis;
        for (auto it = text.begin(), end = text.end(); it != end; ++it) {
            hash ^= * it;
            hash *= fnv_prime;
        }
        return hash;
    }

    std::string to_string(std::floating_point auto value) {
        const auto string = std::to_string(value);
        if (string.find_first_of('.') != std::string::npos) {
            return string;
        }
        return string + ".0";
    }

    std::string to_string(std::integral auto value) {
        return std::to_string(value);
    }

    constexpr std::string_view to_string(bool value) {
        return value == true ? "true" : "false";
    }

}