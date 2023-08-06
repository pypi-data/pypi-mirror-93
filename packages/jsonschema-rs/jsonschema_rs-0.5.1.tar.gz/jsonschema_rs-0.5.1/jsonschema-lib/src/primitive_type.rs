use serde_json::Value;
use std::{convert::TryFrom, fmt, ops::BitOrAssign};

/// For faster error handling in "type" keyword validator we have this enum, to match
/// with it instead of a string.
#[derive(Debug, Clone, Copy)]
pub(crate) enum PrimitiveType {
    Array,
    Boolean,
    Integer,
    Null,
    Number,
    Object,
    String,
}

impl fmt::Display for PrimitiveType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PrimitiveType::Array => write!(f, "array"),
            PrimitiveType::Boolean => write!(f, "boolean"),
            PrimitiveType::Integer => write!(f, "integer"),
            PrimitiveType::Null => write!(f, "null"),
            PrimitiveType::Number => write!(f, "number"),
            PrimitiveType::Object => write!(f, "object"),
            PrimitiveType::String => write!(f, "string"),
        }
    }
}

impl TryFrom<&str> for PrimitiveType {
    type Error = ();

    #[inline]
    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value {
            "array" => Ok(PrimitiveType::Array),
            "boolean" => Ok(PrimitiveType::Boolean),
            "integer" => Ok(PrimitiveType::Integer),
            "null" => Ok(PrimitiveType::Null),
            "number" => Ok(PrimitiveType::Number),
            "object" => Ok(PrimitiveType::Object),
            "string" => Ok(PrimitiveType::String),
            _ => Err(()),
        }
    }
}

impl From<&Value> for PrimitiveType {
    fn from(instance: &Value) -> Self {
        match instance {
            Value::Null => PrimitiveType::Null,
            Value::Bool(_) => PrimitiveType::Boolean,
            Value::Number(_) => PrimitiveType::Number,
            Value::String(_) => PrimitiveType::String,
            Value::Array(_) => PrimitiveType::Array,
            Value::Object(_) => PrimitiveType::Object,
        }
    }
}

#[inline(always)]
fn primitive_type_to_bit_map_representation(primitive_type: PrimitiveType) -> u8 {
    match primitive_type {
        PrimitiveType::Array => 1,
        PrimitiveType::Boolean => 2,
        PrimitiveType::Integer => 4,
        PrimitiveType::Null => 8,
        PrimitiveType::Number => 16,
        PrimitiveType::Object => 32,
        PrimitiveType::String => 64,
    }
}

#[inline(always)]
fn bit_map_representation_primitive_type(bit_representation: u8) -> PrimitiveType {
    match bit_representation {
        1 => PrimitiveType::Array,
        2 => PrimitiveType::Boolean,
        4 => PrimitiveType::Integer,
        8 => PrimitiveType::Null,
        16 => PrimitiveType::Number,
        32 => PrimitiveType::Object,
        64 => PrimitiveType::String,
        _ => unreachable!("This should never be possible"),
    }
}

#[derive(Clone, Copy, Debug)]
pub(crate) struct PrimitiveTypesBitMap {
    inner: u8,
}
impl PrimitiveTypesBitMap {
    pub(crate) const fn new() -> Self {
        Self { inner: 0 }
    }

    #[inline]
    pub(crate) fn add_type(mut self, primitive_type: PrimitiveType) -> Self {
        self.inner |= primitive_type_to_bit_map_representation(primitive_type);
        self
    }

    #[inline(always)]
    pub(crate) fn contains_type(self, primitive_type: PrimitiveType) -> bool {
        primitive_type_to_bit_map_representation(primitive_type) & self.inner != 0
    }
}
impl BitOrAssign<PrimitiveType> for PrimitiveTypesBitMap {
    #[inline]
    fn bitor_assign(&mut self, rhs: PrimitiveType) {
        *self = self.add_type(rhs);
    }
}
impl IntoIterator for PrimitiveTypesBitMap {
    type Item = PrimitiveType;
    type IntoIter = PrimitiveTypesBitMapIterator;
    fn into_iter(self) -> Self::IntoIter {
        PrimitiveTypesBitMapIterator {
            range: 1..7,
            bit_map: self,
        }
    }
}
#[cfg(test)]
impl From<Vec<PrimitiveType>> for PrimitiveTypesBitMap {
    fn from(value: Vec<PrimitiveType>) -> Self {
        let mut result = Self::new();
        for primitive_type in value {
            result |= primitive_type;
        }
        result
    }
}

pub(crate) struct PrimitiveTypesBitMapIterator {
    range: std::ops::Range<u8>,
    bit_map: PrimitiveTypesBitMap,
}
impl Iterator for PrimitiveTypesBitMapIterator {
    type Item = PrimitiveType;
    #[allow(clippy::integer_arithmetic)]
    fn next(&mut self) -> Option<Self::Item> {
        loop {
            if let Some(value) = self.range.next() {
                let bit_value = 1 << value;
                if self.bit_map.inner & bit_value != 0 {
                    return Some(bit_map_representation_primitive_type(bit_value));
                }
            } else {
                return None;
            }
        }
    }
}
