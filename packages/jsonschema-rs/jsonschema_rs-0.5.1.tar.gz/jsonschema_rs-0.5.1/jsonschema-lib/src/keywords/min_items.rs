use crate::{
    compilation::{context::CompilationContext, JSONSchema},
    error::{error, no_error, CompilationError, ErrorIterator, ValidationError},
    keywords::CompilationResult,
    validator::Validate,
};
use serde_json::{Map, Value};

pub(crate) struct MinItemsValidator {
    limit: u64,
}

impl MinItemsValidator {
    #[inline]
    pub(crate) fn compile(schema: &Value) -> CompilationResult {
        if let Some(limit) = schema.as_u64() {
            Ok(Box::new(MinItemsValidator { limit }))
        } else {
            Err(CompilationError::SchemaError)
        }
    }
}

impl Validate for MinItemsValidator {
    fn is_valid(&self, _: &JSONSchema, instance: &Value) -> bool {
        if let Value::Array(items) = instance {
            if (items.len() as u64) < self.limit {
                return false;
            }
        }
        true
    }

    fn validate<'a>(&self, _: &'a JSONSchema, instance: &'a Value) -> ErrorIterator<'a> {
        if let Value::Array(items) = instance {
            if (items.len() as u64) < self.limit {
                return error(ValidationError::min_items(instance, self.limit));
            }
        }
        no_error()
    }
}

impl ToString for MinItemsValidator {
    fn to_string(&self) -> String {
        format!("minItems: {}", self.limit)
    }
}

#[inline]
pub(crate) fn compile(
    _: &Map<String, Value>,
    schema: &Value,
    _: &CompilationContext,
) -> Option<CompilationResult> {
    Some(MinItemsValidator::compile(schema))
}
