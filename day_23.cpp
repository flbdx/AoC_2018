#include <cstdint>
#include <cinttypes>
#include <iostream>
#include <exception>
#include <cmath>
#include <optional>

//#include <map>
#include <vector>
#include <algorithm>
#include <tuple>
#include <string>
#include <fstream>

struct Point {
    int64_t x;
    int64_t y;
    int64_t z;
    Point() : x(0), y(0), z(0) {}
    Point(int64_t x_, int64_t y_, int64_t z_) : x(x_), y(y_), z(z_) {}
};

struct Bot : public Point {
    uint64_t r;
    Bot() : Point(), r(0) {}
    Bot(int64_t x_, int64_t y_, int64_t z_, uint64_t r_) : Point(x_, y_, z_), r(r_) {};
};

template<typename T> static inline typename std::make_unsigned<T>::type abs(const T &v) {
    return (v >= T(0)) ? v : -v;
}

template<typename T>
static inline uint64_t manhattan(const T &p) {
    return abs(p.x) + abs(p.y) + abs(p.z);
}

template<typename T1, typename T2>
static inline uint64_t manhattan(const T1 &p1, const T2 &p2) {
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z);
}

static bool read_input(const std::string &filename, std::vector<Bot> &bots) {
    bots.clear();

    std::ifstream ifs(filename, std::ios::binary);
    if (!ifs.is_open()) {
        fprintf(stderr, "Impossible d'ouvrir le fichier %s\n", filename.c_str());
        return false;
    }

    for (std::string line; std::getline(ifs, line); ) {
        if (line.size() > 0 && line.back() == '\n') {
            line.pop_back();
            if (line.size() > 0 && line.back() == '\r') {
                line.pop_back();
            }
        }
        if (line.size() == 0) {
            continue;
        }

        int64_t x,y,z;
        uint64_t r;
        if (sscanf(line.c_str(), "pos=<%" PRId64 ",%" PRId64 ",%" PRIu64">, r=%" PRId64, &x, &y, &z, &r) != 4) {
            continue;
        }
        bots.emplace_back(x,y,z,r);
    }
    return true;
}

static unsigned int work_p1(const std::string &filename) {
    std::vector<Bot> bots;
    if (!read_input(filename, bots)) {
        fprintf(stderr, "Erreur de lecture de %s\n", filename.c_str());
        return -1;
    }

    // find the bot with the highest range
    uint64_t max_range = 0;
    Bot best_bot;
    for (const auto &p : bots) {
        if (p.r > max_range) {
            max_range = p.r;
            best_bot = p;
        }
    }
    // count all bots in range
    unsigned int in_range = 0;
    for (const auto &p : bots) {
        if (manhattan(p, best_bot) <= max_range) {
            in_range ++;
        }
    }
    return in_range;
}

// apply a scale factor to our space, using closest integer rounding
static void apply_scale(const std::vector<Bot> &in, double factor, std::vector<Bot> &out) {
    out.clear();
    out.reserve(in.size());
    for (const auto &p : in) {
        out.emplace_back(
                std::llround(p.x * factor),
                std::llround(p.y * factor),
                std::llround(p.z * factor),
                std::llround(p.r * factor));
    }
}

static uint64_t work_p2(const std::string &filename) {
    std::vector<Bot> bots;
    if (!read_input(filename, bots)) {
        fprintf(stderr, "Erreur de lecture de %s\n", filename.c_str());
        return -1;
    }

    // find our boundaries and ranges on each axis
    uint64_t range_max;
    {
        int64_t min_x, max_x, min_y, max_y, min_z, max_z;
        auto it = bots.begin();
        min_x = max_x = (*it).x;
        min_y = max_y = (*it).y;
        min_z = max_z = (*it).z;
        for (; it != bots.end(); ++it) {
            const auto &p = *it;
            min_x = std::min(min_x, p.x); max_x = std::max(max_x, p.x);
            min_y = std::min(min_y, p.y); max_y = std::max(max_y, p.y);
            min_z = std::min(min_z, p.z); max_z = std::max(max_z, p.z);
        }
        range_max = std::max(max_x - min_x, std::max(max_y - min_y, max_z - min_z));
    }

    std::optional<unsigned int> best_in_range; // current max bots in range
    uint64_t best_distance = uint64_t(-1);  // current best distance from (0,0,0)
    Point best_point;                       // current best point
    uint64_t scan_width = 300;              // for the first pass, we scale the space to a 300x300x300 space
    Point current_pos;                      // current center point (previous best)
    

    auto find_best_point = [&](const std::vector<Bot> &bots) {
        Point p;
        // search a scale_width*scale_width*scale_with cube centered on current_pos
        for (p.x = current_pos.x - scan_width / 2; p.x <= int64_t(current_pos.x + scan_width / 2); ++p.x) {
            for (p.y = current_pos.y - scan_width / 2; p.y <= int64_t(current_pos.y + scan_width / 2); ++p.y) {
                for (p.z = current_pos.z - scan_width / 2; p.z <= int64_t(current_pos.z + scan_width / 2); ++p.z) {
                    unsigned int in_range = 0;
                    for (const auto &b : bots) {
                        if (manhattan(b, p) <= b.r) {
                            in_range++;
                        }
                    }
                    uint64_t p_dist = manhattan(p);
                    if (!best_in_range || (in_range > best_in_range) || (in_range == best_in_range && p_dist < best_distance)) {
                        best_distance = p_dist;
                        best_in_range = in_range;
                        best_point = p;
                    }
                }
            }
        }
    };

    double scale_factor = double(scan_width) / range_max;
    decltype(bots) scaled_bots;

    // the scale factor is double each pass
    while (scale_factor < 1) {
        apply_scale(bots, scale_factor, scaled_bots);
        find_best_point(scaled_bots);

        printf("<%" PRId64 ",%" PRId64 ",%" PRId64 "> %" PRIu64 " : %u\n", best_point.x, best_point.y, best_point.z, best_distance, *best_in_range);
        fflush(stdout);

        if (scale_factor * 2 < 1) {
            current_pos = Point{best_point.x * 2, best_point.y * 2, best_point.z * 2};
            best_in_range.reset();
            scale_factor *= 2;

            // for the following passes, reduce the sampling size
            scan_width = 75;
        }
        else {
            current_pos = Point{int64_t(best_point.x / scale_factor), int64_t(best_point.y / scale_factor), int64_t(best_point.z / scale_factor)};
            break;
        }
    }

    // final pass without scaling
    scan_width = std::min(scan_width, range_max); // restrict for the smol test case
    find_best_point(bots);

    printf("<%" PRId64 ",%" PRId64 ",%" PRId64 "> %" PRIu64 " : %u\n", best_point.x, best_point.y, best_point.z, best_distance, *best_in_range);
    fflush(stdout);

    return best_distance;
}

static bool test_p1() {
    return work_p1("input_23_test_p1") == 7;
}

static bool test_p2() {
    return work_p2("input_23_test_p2") == 36;
}

int main() {
    if (!test_p1()) {
        fprintf(stderr, "Erreur test_p1\n");
    }
    printf("%u\n", work_p1("input_23"));

    if (!test_p2()) {
        fprintf(stderr, "Erreur test_p2\n");
    }
    printf("%" PRIu64 "\n", work_p2("input_23"));

    return 0;
}
