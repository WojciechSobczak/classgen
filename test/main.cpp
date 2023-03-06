#include <iostream>
#include <nlohmann/json.hpp>


#define private public
#include "generated/ImportantData.hpp"
#include "generated/TemplateRichData.hpp"
#undef private

void assertException(const bool assertion, const std::string_view message = "assertion failed") {
    if (assertion == false) {
        throw std::runtime_error(std::string(message));
    }
}

bool templateRichDataTest() {
    // auto data = Veracruz::TemplateRichData();
    // data.convoluted_real = {
    //     {
    //         std::set<std::string>{"1", "2", "3"}, 
    //         { { 200, std::set<int64_t>{4, 5, 6}} }
    //     }
    // };

    // std::cout << data.toDebugJsonString() << std::endl;
    // assertException(data.toDebugJsonString().size() > 0, "TemplateRichData->toDebugJsonString() :: empty string");
    return true;
}

bool importantDataTest() {
    auto data = Veracruz::ImportantData();
    data.countries = { 
        "Poland", 
        "Goland", 
        "Germony" 
    };

    data.countries_of_continents = {
        {
            {"Albania1", "America1", "Angolololo1"},
            {"Albania2", "America2", "Angolololo2"}
        },
        {
            {"Belgium1", "Beligium1", "Belugium1"},
            {"Belgium2", "Beligium2", "Belugium2"}
        },
        {
            {"Poland1", "Paland1", "Paroland1"},
            {"Poland2", "Paland2", "Paroland2"}
        }
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

    try {
        std::cout << std::string('-', 80) << std::endl;
        std::cout << data.toDebugJsonString() << std::endl;
        std::cout << std::string('-', 80) << std::endl;
    } catch(const std::exception& e) {
        std::cerr << e.what() << ": \n toDebugJsonString() malformed \n";
        return false;
    }

    // try {
    //     std::cout << std::string('-', 80) << std::endl;
    //     std::cout << std::to_string(data) << std::endl;
    //     std::cout << std::string('-', 80) << std::endl;
    // } catch(const std::exception& e) {
    //     std::cerr << e.what() << ": \n std::to_string() malformed \n";
    //     return false;
    // }

    // try {
    //     auto json = data.toNlohmannJson();
    //     std::cout << std::string('-', 80) << std::endl;
    //     std::cout << json.dump(2) << std::endl;
    //     std::cout << std::string('-', 80) << std::endl;
        
    //     assertException(json["countries"].is_array(), "ImportantData->countries :: Type mismatch");
    //     assertException(json["cost_money_map"].is_object(), "ImportantData->cost_money_map :: Type mismatch");
    //     assertException(json["cost_currency_map"].is_object(), "ImportantData->cost_currency_map :: Type mismatch");
    //     assertException(json["length"].is_number_float(), "ImportantData->length :: Type mismatch");
    //     assertException(json["size"].is_number_integer(), "ImportantData->size :: Type mismatch");
    // } catch(const std::exception& e) {
    //     std::cerr << e.what() << ": \n toDebugJsonString() malformed \n";
    //     return false;
    // }

    return true;
}

int main(int args, char** argv, char** env) {
    try {
        templateRichDataTest();
        if (importantDataTest() == false) {
            return -1;
        }
    } catch(const std::exception& e) {
        std::cerr << e.what() << '\n';
    }
    return 0;
}
