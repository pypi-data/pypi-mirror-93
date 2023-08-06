//! Validators for `contentMediaType` and `contentEncoding` keywords.
use crate::{
    compilation::{context::CompilationContext, JSONSchema},
    content_encoding::{ContentEncodingCheckType, ContentEncodingConverterType},
    content_media_type::ContentMediaTypeCheckType,
    error::{error, no_error, CompilationError, ErrorIterator, ValidationError},
    keywords::CompilationResult,
    validator::Validate,
};
use serde_json::{Map, Value};

/// Validator for `contentMediaType` keyword.
pub(crate) struct ContentMediaTypeValidator {
    media_type: String,
    func: ContentMediaTypeCheckType,
}

impl ContentMediaTypeValidator {
    #[inline]
    pub(crate) fn compile(media_type: &str, func: ContentMediaTypeCheckType) -> CompilationResult {
        Ok(Box::new(ContentMediaTypeValidator {
            media_type: media_type.to_string(),
            func,
        }))
    }
}

/// Validator delegates validation to the stored function.
impl Validate for ContentMediaTypeValidator {
    fn is_valid(&self, _: &JSONSchema, instance: &Value) -> bool {
        if let Value::String(item) = instance {
            (self.func)(item)
        } else {
            true
        }
    }

    fn validate<'a>(&self, _: &'a JSONSchema, instance: &'a Value) -> ErrorIterator<'a> {
        if let Value::String(item) = instance {
            if (self.func)(item) {
                no_error()
            } else {
                error(ValidationError::content_media_type(
                    instance,
                    &self.media_type,
                ))
            }
        } else {
            no_error()
        }
    }
}

impl ToString for ContentMediaTypeValidator {
    fn to_string(&self) -> String {
        format!("contentMediaType: {}", self.media_type)
    }
}

/// Validator for `contentEncoding` keyword.
pub(crate) struct ContentEncodingValidator {
    encoding: String,
    func: ContentEncodingCheckType,
}

impl ContentEncodingValidator {
    #[inline]
    pub(crate) fn compile(encoding: &str, func: ContentEncodingCheckType) -> CompilationResult {
        Ok(Box::new(ContentEncodingValidator {
            encoding: encoding.to_string(),
            func,
        }))
    }
}

impl Validate for ContentEncodingValidator {
    fn is_valid(&self, _: &JSONSchema, instance: &Value) -> bool {
        if let Value::String(item) = instance {
            (self.func)(item)
        } else {
            true
        }
    }

    fn validate<'a>(&self, _: &'a JSONSchema, instance: &'a Value) -> ErrorIterator<'a> {
        if let Value::String(item) = instance {
            if (self.func)(item) {
                no_error()
            } else {
                error(ValidationError::content_encoding(instance, &self.encoding))
            }
        } else {
            no_error()
        }
    }
}

impl ToString for ContentEncodingValidator {
    fn to_string(&self) -> String {
        format!("contentEncoding: {}", self.encoding)
    }
}

/// Combined validator for both `contentEncoding` and `contentMediaType` keywords.
pub(crate) struct ContentMediaTypeAndEncodingValidator {
    media_type: String,
    encoding: String,
    func: ContentMediaTypeCheckType,
    converter: ContentEncodingConverterType,
}

impl ContentMediaTypeAndEncodingValidator {
    #[inline]
    pub(crate) fn compile(
        media_type: &str,
        encoding: &str,
        func: ContentMediaTypeCheckType,
        converter: ContentEncodingConverterType,
    ) -> CompilationResult {
        Ok(Box::new(ContentMediaTypeAndEncodingValidator {
            media_type: media_type.to_string(),
            encoding: encoding.to_string(),
            func,
            converter,
        }))
    }
}

/// Decode the input value & check media type
impl Validate for ContentMediaTypeAndEncodingValidator {
    fn is_valid(&self, _: &JSONSchema, instance: &Value) -> bool {
        if let Value::String(item) = instance {
            match (self.converter)(item) {
                Ok(None) | Err(_) => false,
                Ok(Some(converted)) => (self.func)(&converted),
            }
        } else {
            true
        }
    }

    fn validate<'a>(&self, _: &'a JSONSchema, instance: &'a Value) -> ErrorIterator<'a> {
        if let Value::String(item) = instance {
            match (self.converter)(item) {
                Ok(None) => error(ValidationError::content_encoding(instance, &self.encoding)),
                Ok(Some(converted)) => {
                    if (self.func)(&converted) {
                        no_error()
                    } else {
                        error(ValidationError::content_media_type(
                            instance,
                            &self.media_type,
                        ))
                    }
                }
                Err(e) => error(e),
            }
        } else {
            no_error()
        }
    }
}

impl ToString for ContentMediaTypeAndEncodingValidator {
    fn to_string(&self) -> String {
        format!(
            "{{contentMediaType: {}, contentEncoding: {}}}",
            self.media_type, self.encoding
        )
    }
}

#[inline]
pub(crate) fn compile_media_type(
    schema: &Map<String, Value>,
    subschema: &Value,
    context: &CompilationContext,
) -> Option<CompilationResult> {
    match subschema {
        Value::String(media_type) => {
            let func = match context.config.content_media_type_check(media_type.as_str()) {
                Some(f) => f,
                None => return None,
            };
            if let Some(content_encoding) = schema.get("contentEncoding") {
                match content_encoding {
                    Value::String(content_encoding) => {
                        let converter = match context
                            .config
                            .content_encoding_convert(content_encoding.as_str())
                        {
                            Some(f) => f,
                            None => return None,
                        };
                        Some(ContentMediaTypeAndEncodingValidator::compile(
                            media_type,
                            content_encoding,
                            func,
                            converter,
                        ))
                    }
                    _ => Some(Err(CompilationError::SchemaError)),
                }
            } else {
                Some(ContentMediaTypeValidator::compile(media_type, func))
            }
        }
        _ => Some(Err(CompilationError::SchemaError)),
    }
}

#[inline]
pub(crate) fn compile_content_encoding(
    schema: &Map<String, Value>,
    subschema: &Value,
    context: &CompilationContext,
) -> Option<CompilationResult> {
    // Performed during media type validation
    if schema.get("contentMediaType").is_some() {
        // TODO. what if media type is not supported?
        return None;
    }
    match subschema {
        Value::String(content_encoding) => {
            let func = match context
                .config
                .content_encoding_check(content_encoding.as_str())
            {
                Some(f) => f,
                None => return None,
            };
            Some(ContentEncodingValidator::compile(content_encoding, func))
        }
        _ => Some(Err(CompilationError::SchemaError)),
    }
}
