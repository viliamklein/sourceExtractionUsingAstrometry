CXX       := g++
CXX_FLAGS := -std=c++17 -Wall -pg

BIN     := build
SRC     := src
INCLUDE := include
LIBINC := lib
# ASIOINC := /home/viliam/sources/asio-1.18.1/include/
# JSONINC := /home/viliam/sources/json/include/
# CCFITSINC := /usr/local/include/CCfits/
ASTROMETRYINC := /usr/local/astrometry/include/

LDFLAGS := -lpthread -lcfitsio -ldl

LIBRARIES := -L/usr/local/astrometry/lib/ -lanutils -lanbase -lanfiles -lqfits -lkd -lcatalogs 
EXECUTABLE  := sourceTest
EXECUTABLE_DEBUG  := sourceTest_debug


all: $(BIN)/$(EXECUTABLE)

run: clean all
	clear
	./$(BIN)/$(EXECUTABLE)

$(BIN)/$(EXECUTABLE): $(SRC)/*.cpp
	$(CXX) $(CXX_FLAGS) -O2 -I$(INCLUDE) -I$(ASTROMETRYINC) $^ -o $@ \
	$(LIBRARIES) $(LDFLAGS)


debug: $(BIN)/$(EXECUTABLE_DEBUG)

rundebug: clean all
	clear
	./$(BIN)/$(EXECUTABLE_DEBUG)

$(BIN)/$(EXECUTABLE_DEBUG): $(SRC)/*.cpp
	$(CXX) $(CXX_FLAGS) -ggdb -I$(INCLUDE) -I$(ASTROMETRYINC) $^ -o $@ \
	$(LIBRARIES) $(LDFLAGS)

clean:
	-rm $(BIN)/*