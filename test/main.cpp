#include <iostream>
#include <nlohmann/json.hpp>


#define private public
#include "generated/ImportantData.hpp"
#undef private

void assertException(const bool assertion, const std::string_view message = "assertion failed") {
    if (assertion == false) {
        throw std::runtime_error(std::string(message));
    }
}

bool importantDataTest() {
    auto data = Veracruz::ImportantData();
    data.countries = { 
        "Poland", 
        "Goland", 
        "Germony" 
    };
    data.cost_money_map = {
        { "PLN", 2.4 },
        { "EUR", 1.6 },
        { "CHR", 0.02 }
    };
    data.cost_currency_map = {
        { "EUR", "1.6 str" },
        { "PLN", "2.4 str" },
        { "CHR", "0.02 str" }
    };
    data.length = 100.f;
    data.size = UINT_MAX;

    constexpr auto ensureImportantDataState = [](const nlohmann::json& json) {
        assertException(json["countries"].is_array(), "ImportantData->countries :: Type mismatch");
        assertException(json["cost_money_map"].is_object(), "ImportantData->cost_money_map :: Type mismatch");
        assertException(json["cost_currency_map"].is_object(), "ImportantData->cost_currency_map :: Type mismatch");
        assertException(json["length"].is_number_float(), "ImportantData->length :: Type mismatch");
        assertException(json["size"].is_number_integer(), "ImportantData->size :: Type mismatch");
    };

    try {
        auto toJsonJson = nlohmann::json::parse(data.toJsonString());
        ensureImportantDataState(toJsonJson);
    } catch(const std::exception& e) {
        std::cerr << e.what() << ": \n toJsonString() malformed \n";
        return false;
    }

    try {
        auto toStringJson = nlohmann::json::parse(std::to_string(data));
        ensureImportantDataState(toStringJson);
    } catch(const std::exception& e) {
        std::cerr << e.what() << ": \n std::to_string() malformed \n";
        return false;
    }

    try {
        auto toStringJson = nlohmann::json::parse(std::to_string(data));
        auto toNlohmannJson = data.toNlohmannJson();

        if (toStringJson != toNlohmannJson) {
            throw std::exception("nlohmann::json::parse and data.toNlohmannJson() does not provide the same data");
        }
    } catch(const std::exception& e) {
        std::cerr << e.what() << ": \n toNlohmannJson() malformed \n";
        return false;
    }

    return true;
}

int main(int args, char** argv, char** env) {
    if (importantDataTest() == false) {
        return -1;
    }
    return 0;
}
