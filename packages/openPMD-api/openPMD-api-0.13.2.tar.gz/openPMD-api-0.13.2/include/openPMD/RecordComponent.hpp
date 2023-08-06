/* Copyright 2017-2020 Fabian Koller
 *
 * This file is part of openPMD-api.
 *
 * openPMD-api is free software: you can redistribute it and/or modify
 * it under the terms of of either the GNU General Public License or
 * the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * openPMD-api is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License and the GNU Lesser General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License
 * and the GNU Lesser General Public License along with openPMD-api.
 * If not, see <http://www.gnu.org/licenses/>.
 */
#pragma once

#include "openPMD/backend/BaseRecordComponent.hpp"
#include "openPMD/auxiliary/ShareRaw.hpp"
#include "openPMD/Dataset.hpp"

#include <cmath>
#include <memory>
#include <limits>
#include <queue>
#include <string>
#include <sstream>
#include <stdexcept>
#include <type_traits>
#include <vector>
#include <array>

// expose private and protected members for invasive testing
#ifndef OPENPMD_protected
#   define OPENPMD_protected protected
#endif


namespace openPMD
{
namespace traits
{
/** Emulate in the C++17 concept ContiguousContainer
 *
 * Users can implement this trait for a type to signal it can be used as
 * contiguous container.
 *
 * See:
 *   https://en.cppreference.com/w/cpp/named_req/ContiguousContainer
 */
template< typename T >
struct IsContiguousContainer
{
    static constexpr bool value = false;
};

template< typename T_Value >
struct IsContiguousContainer< std::vector< T_Value > >
{
    static constexpr bool value = true;
};

template<
    typename T_Value,
    std::size_t N
>
struct IsContiguousContainer< std::array< T_Value, N > >
{
    static constexpr bool value = true;
};
} // namespace traits

class RecordComponent : public BaseRecordComponent
{
    template<
            typename T,
            typename T_key,
            typename T_container
    >
    friend class Container;
    friend class Iteration;
    friend class ParticleSpecies;
    template< typename T_elem >
    friend class BaseRecord;
    friend class Record;
    friend class Mesh;

public:
    enum class Allocation
    {
        USER,
        API,
        AUTO
    }; // Allocation

    RecordComponent& setUnitSI(double);

    RecordComponent& resetDataset(Dataset);

    uint8_t getDimensionality() const;
    Extent getExtent() const;

    /** Create a dataset with regular extent and constant value
     *
     * In a constant record component, the value for each date in its extent is
     * the same. Implemented by storing only a constant value as meta-data.
     *
     * @tparam T type of the stored value
     * @return A reference to this RecordComponent.
     */
    template< typename T >
    RecordComponent& makeConstant(T);

    /** Create a dataset with zero extent in each dimension.
     *
     * Implemented by creating a constant record component with
     * a dummy value (default constructor of the respective datatype).
     * @param dimensions The number of dimensions. Must be greater than
     *                   zero.
     * @return A reference to this RecordComponent.
     */
    template< typename T >
    RecordComponent& makeEmpty( uint8_t dimensions );

    /**
     * @brief Non-template overload of RecordComponent::makeEmpty().
     * Uses the passed openPMD datatype to determine the template parameter.
     *
     * @param dt The datatype of which to create an empty dataset.
     * @param dimensions The dimensionality of the dataset.
     * @return RecordComponent&
     */
    RecordComponent& makeEmpty( Datatype dt, uint8_t dimensions );

    /** Returns true if this is an empty record component
     *
     * An empty record component has a defined dimensionality but zero extent
     * and no value(s) stored in it.
     *
     * @return true if an empty record component
     */
    bool empty() const;

    /** Load and allocate a chunk of data
     *
     * Set offset to {0u} and extent to {-1u} for full selection.
     *
     * If offset is non-zero and extent is {-1u} the leftover extent in the
     * record component will be selected.
     */
    template< typename T >
    std::shared_ptr< T > loadChunk(
        Offset = {0u},
        Extent = {-1u},
        double targetUnitSI = std::numeric_limits< double >::quiet_NaN() );

    /** Load a chunk of data into pre-allocated memory
     *
     * shared_ptr for data must be pre-allocated, contiguous and large enough for extent
     *
     * Set offset to {0u} and extent to {-1u} for full selection.
     *
     * If offset is non-zero and extent is {-1u} the leftover extent in the
     * record component will be selected.
     */
    template< typename T >
    void loadChunk(
        std::shared_ptr< T >,
        Offset,
        Extent,
        double targetUnitSI = std::numeric_limits< double >::quiet_NaN() );

    template< typename T >
    void storeChunk(std::shared_ptr< T >, Offset, Extent);

    template< typename T_ContiguousContainer >
    typename std::enable_if<
        traits::IsContiguousContainer< T_ContiguousContainer >::value
    >::type
    storeChunk(T_ContiguousContainer &, Offset = {0u}, Extent = {-1u});

    static constexpr char const * const SCALAR = "\vScalar";

    virtual ~RecordComponent() = default;

OPENPMD_protected:
    RecordComponent();

    void readBase();

    std::shared_ptr< std::queue< IOTask > > m_chunks;
    std::shared_ptr< Attribute > m_constantValue;
    std::shared_ptr< bool > m_isEmpty = std::make_shared< bool >( false );

private:
    void flush(std::string const&);
    virtual void read();

    /**
     * Internal method to be called by all methods that create an empty dataset.
     *
     * @param d The dataset description. Must have nonzero dimensions.
     * @return Reference to this RecordComponent instance.
     */
    RecordComponent& makeEmpty( Dataset d );

    /**
     * @brief Check recursively whether this RecordComponent is dirty.
     *        It is dirty if any attribute or dataset is read from or written to
     *        the backend.
     *
     * @return true If dirty.
     * @return false Otherwise.
     */
    bool
    dirtyRecursive() const;

protected:
    /**
     * Make sure to parse a RecordComponent only once.
     */
    std::shared_ptr< bool > hasBeenRead = std::make_shared< bool >( false );
}; // RecordComponent


template< typename T >
inline RecordComponent&
RecordComponent::makeConstant(T value)
{
    if( written() )
        throw std::runtime_error("A recordComponent can not (yet) be made constant after it has been written.");

    *m_constantValue = Attribute(value);
    *m_isConstant = true;
    return *this;
}

template< typename T >
inline RecordComponent&
RecordComponent::makeEmpty( uint8_t dimensions )
{
    return makeEmpty( Dataset(
        determineDatatype< T >(),
        Extent( dimensions, 0 ) ) );
}

template< typename T >
inline std::shared_ptr< T >
RecordComponent::loadChunk(Offset o, Extent e, double targetUnitSI)
{
    uint8_t dim = getDimensionality();

    // default arguments
    //   offset = {0u}: expand to right dim {0u, 0u, ...}
    Offset offset = o;
    if( o.size() == 1u && o.at(0) == 0u && dim > 1u )
        offset = Offset(dim, 0u);

    //   extent = {-1u}: take full size
    Extent extent(dim, 1u);
    if( e.size() == 1u && e.at(0) == -1u )
    {
        extent = getExtent();
        for( uint8_t i = 0u; i < dim; ++i )
            extent[i] -= offset[i];
    }
    else
        extent = e;

    uint64_t numPoints = 1u;
    for( auto const& dimensionSize : extent )
        numPoints *= dimensionSize;

    auto newData = std::shared_ptr<T>(new T[numPoints], []( T *p ){ delete [] p; });
    loadChunk(newData, offset, extent, targetUnitSI);
    return newData;
}

template< typename T >
inline void
RecordComponent::loadChunk(std::shared_ptr< T > data, Offset o, Extent e, double targetUnitSI)
{
    if( !std::isnan(targetUnitSI) )
        throw std::runtime_error("unitSI scaling during chunk loading not yet implemented");
    Datatype dtype = determineDatatype(data);
    if( dtype != getDatatype() )
        if( !isSameInteger< T >( dtype ) &&
            !isSameFloatingPoint< T >( dtype ) &&
            !isSameComplexFloatingPoint< T >( dtype ) )
            throw std::runtime_error("Type conversion during chunk loading not yet implemented");

    uint8_t dim = getDimensionality();

    // default arguments
    //   offset = {0u}: expand to right dim {0u, 0u, ...}
    Offset offset = o;
    if( o.size() == 1u && o.at(0) == 0u && dim > 1u )
        offset = Offset(dim, 0u);

    //   extent = {-1u}: take full size
    Extent extent(dim, 1u);
    if( e.size() == 1u && e.at(0) == -1u )
    {
        extent = getExtent();
        for( uint8_t i = 0u; i < dim; ++i )
            extent[i] -= offset[i];
    }
    else
        extent = e;

    if( extent.size() != dim || offset.size() != dim )
    {
        std::ostringstream oss;
        oss << "Dimensionality of chunk ("
            << "offset=" << offset.size() << "D, "
            << "extent=" << extent.size() << "D) "
            << "and record component ("
            << int(dim) << "D) "
            << "do not match.";
        throw std::runtime_error(oss.str());
    }
    Extent dse = getExtent();
    for( uint8_t i = 0; i < dim; ++i )
        if( dse[i] < offset[i] + extent[i] )
            throw std::runtime_error("Chunk does not reside inside dataset (Dimension on index " + std::to_string(i)
                                     + ". DS: " + std::to_string(dse[i])
                                     + " - Chunk: " + std::to_string(offset[i] + extent[i])
                                     + ")");
    if( !data )
        throw std::runtime_error("Unallocated pointer passed during chunk loading.");

    if( constant() )
    {
        uint64_t numPoints = 1u;
        for( auto const& dimensionSize : extent )
            numPoints *= dimensionSize;

        T value = m_constantValue->get< T >();

        T* raw_ptr = data.get();
        std::fill(raw_ptr, raw_ptr + numPoints, value);
    } else
    {
        Parameter< Operation::READ_DATASET > dRead;
        dRead.offset = offset;
        dRead.extent = extent;
        dRead.dtype = getDatatype();
        dRead.data = std::static_pointer_cast< void >(data);
        m_chunks->push(IOTask(this, dRead));
    }
}

template< typename T >
inline void
RecordComponent::storeChunk(std::shared_ptr<T> data, Offset o, Extent e)
{
    if( constant() )
        throw std::runtime_error("Chunks cannot be written for a constant RecordComponent.");
    if( empty() )
        throw std::runtime_error("Chunks cannot be written for an empty RecordComponent.");
    if( !data )
        throw std::runtime_error("Unallocated pointer passed during chunk store.");
    Datatype dtype = determineDatatype(data);
    if( dtype != getDatatype() )
    {
        std::ostringstream oss;
        oss << "Datatypes of chunk data ("
            << dtype
            << ") and record component ("
            << getDatatype()
            << ") do not match.";
        throw std::runtime_error(oss.str());
    }
    uint8_t dim = getDimensionality();
    if( e.size() != dim || o.size() != dim )
    {
        std::ostringstream oss;
        oss << "Dimensionality of chunk ("
            << "offset=" << o.size() << "D, "
            << "extent=" << e.size() << "D) "
            << "and record component ("
            << int(dim) << "D) "
            << "do not match.";
        throw std::runtime_error(oss.str());
    }
    Extent dse = getExtent();
    for( uint8_t i = 0; i < dim; ++i )
        if( dse[i] < o[i] + e[i] )
            throw std::runtime_error("Chunk does not reside inside dataset (Dimension on index " + std::to_string(i)
                                     + ". DS: " + std::to_string(dse[i])
                                     + " - Chunk: " + std::to_string(o[i] + e[i])
                                     + ")");

    Parameter< Operation::WRITE_DATASET > dWrite;
    dWrite.offset = o;
    dWrite.extent = e;
    dWrite.dtype = dtype;
    /* std::static_pointer_cast correctly reference-counts the pointer */
    dWrite.data = std::static_pointer_cast< void const >(data);
    m_chunks->push(IOTask(this, dWrite));
}

template< typename T_ContiguousContainer >
inline typename std::enable_if<
    traits::IsContiguousContainer< T_ContiguousContainer >::value
>::type
RecordComponent::storeChunk(T_ContiguousContainer & data, Offset o, Extent e)
{
    uint8_t dim = getDimensionality();

    // default arguments
    //   offset = {0u}: expand to right dim {0u, 0u, ...}
    Offset offset = o;
    if( o.size() == 1u && o.at(0) == 0u && dim > 1u )
        offset = Offset(dim, 0u);

    //   extent = {-1u}: take full size
    Extent extent(dim, 1u);
    //   avoid outsmarting the user:
    //   - stdlib data container implement 1D -> 1D chunk to write
    if( e.size() == 1u && e.at(0) == -1u && dim == 1u )
        extent.at(0) = data.size();
    else
        extent = e;

    storeChunk(shareRaw(data), offset, extent);
}
} // namespace openPMD
